import json
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST,require_GET
from django.utils import timezone
from django.contrib.auth.models import User
from .models import *
from .permissions import *

def data(request):
 try:return json.loads(request.body or '{}')
 except:return {}
def err(message,status=400):return JsonResponse({'ok':False,'error':message},status=status)
def task_access(request,id,delete=False):
 t=Task.objects.filter(id=id).first()
 if not t:return None,err('کار پیدا نشد.',404)
 if not (can_user_delete_task(request.user,t) if delete else can_user_edit_task(request.user,t)):return None,err('اجازه انجام این کار را ندارید.',403)
 return t,None
@login_required
@require_POST
def create_task(request):
 d=data(request); task_list=TaskList.objects.filter(id=d.get('task_list_id'),owner=request.user).first() if d.get('task_list_id') else None
 project=Project.objects.filter(id=d.get('project_id')).first() if d.get('project_id') else None
 if d.get('project_id') and not project:return err('پروژه نامعتبر است.')
 if not can_create(request.user,project):return err('اجازه ساخت ندارید.',403)
 title=d.get('title','').strip()
 if not title:return err('عنوان ضروری است.')
 due=None
 if d.get('due_date'):
  try: due=datetime.fromisoformat(d['due_date'].replace('Z','+00:00')); due=timezone.make_aware(due) if timezone.is_naive(due) else due
  except ValueError:return err('تاریخ نامعتبر است.')
 t=Task.objects.create(title=title,description=d.get('description',''),owner=request.user,project=project,task_list=task_list,due_date=due,task_type=d.get('task_type','normal'),position_x=d.get('x'),position_y=d.get('y'))
 for i,s in enumerate(d.get('subtasks',[])):
  if str(s).strip():SubTask.objects.create(task=t,title=str(s).strip(),order=i)
 return JsonResponse({'ok':True,'id':t.id,'color':t.get_status_color()})
@login_required
@require_POST
def move_task(request,id):
 t,e=task_access(request,id)
 if e:return e
 d=data(request)
 try:t.position_x=float(d['x']);t.position_y=float(d['y']);t.save(update_fields=['position_x','position_y'])
 except (KeyError,TypeError,ValueError):return err('موقعیت نامعتبر است.')
 return JsonResponse({'ok':True})
@login_required
@require_POST
def status_task(request,id):
 t,e=task_access(request,id)
 if e:return e
 st=data(request).get('status')
 if st not in ('todo','in_progress','done'):return err('وضعیت نامعتبر است.')
 blockers=t.incoming_dependencies.exclude(from_task__status='done')
 if st in ('in_progress','done') and blockers.exists():return err('مسدود شده توسط: '+blockers.first().from_task.title)
 if st=='done' and t.subtasks.filter(is_done=False).exists():return err('هنوز زیرکار ناتمام دارید.')
 if st=='done' and data(request).get('confirm')!='آره':return err('برای تأیید، «آره» را وارد کنید.')
 t.status=st
 if st=='in_progress' and not t.started_at:t.started_at=timezone.now()
 t.refresh_color();t.save()
 if st=='done':
  for dep in t.outgoing_dependencies.select_related('to_task'):
   goal=dep.to_task
   if goal.task_type=='goal' and not goal.incoming_dependencies.exclude(from_task__status='done').exists():
    goal.status='done';goal.refresh_color();goal.save();
 return JsonResponse({'ok':True,'color':t.display_color,'goal_completed':st=='done'})
@login_required
@require_POST
def toggle_subtask(request,id):
 s=SubTask.objects.filter(id=id).select_related('task').first()
 if not s:return err('زیرکار پیدا نشد.',404)
 if not can_user_edit_task(request.user,s.task):return err('مجاز نیستید.',403)
 d=data(request);s.is_done=bool(d['is_done']) if 'is_done' in d else not s.is_done;s.save(update_fields=['is_done']);return JsonResponse({'ok':True,'done':s.is_done})
@login_required
@require_POST
def dep_create(request):
 d=data(request); a=Task.objects.filter(id=d.get('from_task')).first();b=Task.objects.filter(id=d.get('to_task')).first()
 if not a or not b or a==b:return err('اتصال نامعتبر است.')
 if a.project_id!=b.project_id:return err('فقط وظایف یک بوم قابل اتصال‌اند.')
 if not can_user_edit_task(request.user,a) or not can_user_edit_task(request.user,b):return err('مجاز نیستید.',403)
 if a.task_type=='goal':return err('هدف فقط اتصال ورودی می‌پذیرد.')
 TaskDependency.objects.get_or_create(from_task=a,to_task=b);return JsonResponse({'ok':True})
@login_required
@require_POST
def label_create(request):
 d=data(request);p=Project.objects.filter(id=d.get('project_id')).first() if d.get('project_id') else None
 if not can_create(request.user,p):return err('مجاز نیستید.',403)
 l=StudioLabel.objects.create(owner=request.user,project=p,text=d.get('text','برچسب'),position_x=d.get('x',100),position_y=d.get('y',100));return JsonResponse({'ok':True,'id':l.id})
@login_required
@require_POST
def invite(request):
 d=data(request);p=Project.objects.filter(id=d.get('project_id'),owner=request.user).first();u=User.objects.filter(username=d.get('username')).first()
 if not p or not u:return err('پروژه یا کاربر پیدا نشد.')
 c,_=ProjectCollaborator.objects.update_or_create(project=p,user=u,defaults={'status':'pending','invited_by':request.user});ProjectRole.objects.get_or_create(collaborator=c);return JsonResponse({'ok':True})
@login_required
@require_POST
def respond(request):
 c=ProjectCollaborator.objects.filter(id=data(request).get('collaborator_id'),user=request.user).first()
 if not c:return err('دعوت پیدا نشد.',404)
 c.status='accepted' if data(request).get('accept') else 'declined';c.save();return JsonResponse({'ok':True})
@login_required
@require_POST
def role(request):
 d=data(request);c=ProjectCollaborator.objects.filter(id=d.get('collaborator_id'),project__owner=request.user).first()
 if not c:return err('مجاز نیستید.',403)
 r,_=ProjectRole.objects.get_or_create(collaborator=c)
 for x in ('can_edit','can_delete','can_create'):setattr(r,x,bool(d.get(x)))
 r.save();r.allowed_tags.set(Tag.objects.filter(id__in=d.get('allowed_tags',[]),project=c.project));return JsonResponse({'ok':True})
@login_required
@require_POST
def heartbeat(request):
 p=request.user.profile;now=timezone.now()
 if not p.last_seen or (now-p.last_seen).total_seconds()>=15:p.last_seen=now;p.save(update_fields=['last_seen'])
 return JsonResponse({'ok':True})
@login_required
@require_GET
def presence(request,id):
 p=Project.objects.filter(id=id).first()
 if not p or not can_view_project(request.user,p):return err('مجاز نیستید.',403)
 users=[p.owner]+[x.user for x in p.collaborators.filter(status='accepted').select_related('user__profile')]
 now=timezone.now();return JsonResponse({'users':[{'username':u.username,'online':bool(u.profile.last_seen and (now-u.profile.last_seen).total_seconds()<60)} for u in users]})
@login_required
@require_GET
def calendar_events(request):
 try:y=int(request.GET['year']);m=int(request.GET['month'])
 except:return err('ماه نامعتبر است.')
 tasks=Task.objects.filter(owner=request.user,due_date__year=y,due_date__month=m)
 events=CalendarEvent.objects.filter(starts_at__year=y,starts_at__month=m,created_by=request.user)
 return JsonResponse({'tasks':[{'title':t.title,'date':t.due_date.isoformat(),'color':t.get_status_color()} for t in tasks.distinct()],'events':[{'title':e.title,'date':e.starts_at.isoformat(),'type':e.type} for e in events.distinct()]})
@login_required
@require_POST
def event_create(request):
 d=data(request);p=Project.objects.filter(id=d.get('project_id')).first() if d.get('project_id') else None
 if not can_create(request.user,p):return err('مجاز نیستید.',403)
 try:
  dt=datetime.fromisoformat(d['starts_at'].replace('Z','+00:00'));dt=timezone.make_aware(dt) if timezone.is_naive(dt) else dt
  end_raw=d.get('ends_at');end=datetime.fromisoformat(end_raw.replace('Z','+00:00')) if end_raw else None;end=timezone.make_aware(end) if end and timezone.is_naive(end) else end
 except:return err('تاریخ یا زمان نامعتبر است.')
 e=CalendarEvent.objects.create(project=p,title=d.get('title','رویداد'),type=d.get('type','event'),starts_at=dt,ends_at=end,created_by=request.user)
 return JsonResponse({'ok':True,'id':e.id})
@login_required
@require_POST
def delete_task(request,id):
 t,e=task_access(request,id,delete=True)
 if e:return e
 t.delete()
 return JsonResponse({'ok':True})
@login_required
@require_POST
def task_edit(request,id):
 t,e=task_access(request,id)
 if e:return e
 d=data(request);t.title=d.get('title',t.title).strip() or t.title;t.description=d.get('description',t.description);t.save(update_fields=['title','description']);return JsonResponse({'ok':True})
@login_required
@require_POST
def task_extend(request,id):
 t,e=task_access(request,id)
 if e:return e
 d=data(request)
 try:
  dt=datetime.fromisoformat(d['extension_due_date'].replace('Z','+00:00'));t.extension_due_date=timezone.make_aware(dt) if timezone.is_naive(dt) else dt;t.save(update_fields=['extension_due_date'])
 except:return err('زمان کمکی نامعتبر است.')
 return JsonResponse({'ok':True})
@login_required
@require_POST
def project_action(request,id,action):
 p=Project.objects.filter(id=id,owner=request.user).first()
 if not p:return err('مجاز نیستید.',403)
 d=data(request)
 if action in ('delete','complete') and d.get('confirm')!='آره':return err('برای تأیید، «آره» را وارد کنید.')
 if action=='delete':p.delete();return JsonResponse({'ok':True})
 if action=='complete':
  if p.tasks.exclude(status='done').exists() or SubTask.objects.filter(task__project=p,is_done=False).exists():return err('هنوز وظیفه یا زیرکار ناتمام وجود دارد.')
  p.status='done';p.completed_at=timezone.now();p.save(update_fields=['status','completed_at']);return JsonResponse({'ok':True})
 p.name=d.get('name',p.name).strip() or p.name;p.description=d.get('description',p.description);p.save(update_fields=['name','description']);return JsonResponse({'ok':True})
@login_required
@require_POST
def workspace_move(request):
 d=data(request);kind=d.get('kind');obj=(Task.objects.filter(id=d.get('id')).first() if kind=='task' else Project.objects.filter(id=d.get('id')).first())
 if not obj:return err('آیتم پیدا نشد.',404)
 if kind=='task' and not can_user_edit_task(request.user,obj):return err('مجاز نیستید.',403)
 if kind=='project' and obj.owner_id!=request.user.id:return err('مجاز نیستید.',403)
 try:obj.workspace_position=float(d.get('position',0));obj.save(update_fields=['workspace_position'])
 except:return err('موقعیت نامعتبر است.')
 return JsonResponse({'ok':True})

@login_required
@require_POST
def task_list_create(request):
 d=data(request);count=TaskList.objects.filter(owner=request.user).count();name=d.get('name','').strip() or f'کار {count+1}';l=TaskList.objects.create(owner=request.user,name=name);return JsonResponse({'ok':True,'id':l.id,'name':l.name})
@login_required
@require_POST
def task_list_delete(request,id):
    task_list=TaskList.objects.filter(id=id,owner=request.user).first()
    if not task_list:return err('باکس پیدا نشد.',404)
    task_list.delete()
    return JsonResponse({'ok':True})
