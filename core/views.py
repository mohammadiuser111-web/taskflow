import jdatetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import *
from .forms import *
from .permissions import *
def ctx(request,**kw):
 kw['jalali_today']=jdatetime.date.today().strftime('%Y/%m/%d');return kw
def register(request):
 if request.method=='POST':
  f=RegisterForm(request.POST)
  if f.is_valid():
   u=User.objects.create_user(f.cleaned_data['username'],password=f.cleaned_data['password']);login(request,u);return redirect('dashboard')
 else:f=RegisterForm()
 return render(request,'auth/register.html',ctx(request,form=f))
@login_required
def dashboard(request):
 pending=ProjectCollaborator.objects.filter(user=request.user,status='pending').select_related('project')
 tasks=Task.objects.filter(owner=request.user,project__isnull=True).prefetch_related('tags','subtasks')
 projects=Project.objects.filter(owner=request.user)|Project.objects.filter(collaborators__user=request.user,collaborators__status='accepted')
 my_tasks=(Task.objects.filter(owner=request.user)|Task.objects.filter(project__owner=request.user)|Task.objects.filter(project__collaborators__user=request.user,project__collaborators__status='accepted')).select_related('project','project__group').prefetch_related('tags','subtasks').distinct().order_by('display_color','due_date','created_at')
 return render(request,'dashboard.html',ctx(request,tasks=tasks.distinct(),my_tasks=my_tasks,projects=projects.distinct(),groups=Group.objects.filter(owner=request.user).prefetch_related('projects'),pending=pending))
@login_required
def profile(request):
 p=request.user.profile
 if request.method=='POST':
  f=ProfileForm(request.POST,request.FILES,instance=p)
  if f.is_valid():f.save();return redirect('profile')
 else:f=ProfileForm(instance=p)
 return render(request,'auth/profile.html',ctx(request,form=f,profile=p,bot_username=__import__('os').environ.get('TELEGRAM_BOT_USERNAME','YOUR_BOT')))
@login_required
def create_project(request):
 if request.method=='POST':
  f=ProjectForm(request.POST)
  f.fields['group'].queryset=Group.objects.filter(owner=request.user)
  if f.is_valid():p=f.save(commit=False);p.owner=request.user;p.save();return redirect('project_detail',p.id)
 return redirect('dashboard')
@login_required
def create_group(request):
 if request.method=='POST':
  f=GroupForm(request.POST)
  if f.is_valid():
   g=f.save(commit=False);g.owner=request.user;g.save()
 return redirect('dashboard')
@login_required
def project_detail(request,id):
 p=get_object_or_404(Project,id=id)
 if not can_view_project(request.user,p):return redirect('dashboard')
 tasks=p.tasks.prefetch_related('tags','subtasks').all();return render(request,'project_detail.html',ctx(request,project=p,tasks=tasks,tags=p.tags.all(),projects=[p],can_edit=can_create(request.user,p),is_owner=p.owner_id==request.user.id))
@login_required
def studio(request,project_id=None):
 p=get_object_or_404(Project,id=project_id) if project_id else None
 if p and not can_view_project(request.user,p):return redirect('dashboard')
 tasks=(p.tasks if p else Task.objects.filter(owner=request.user,project__isnull=True)).prefetch_related('tags')
 labels=StudioLabel.objects.filter(project=p) if p else StudioLabel.objects.filter(project__isnull=True,owner=request.user)
 deps=TaskDependency.objects.filter(from_task__in=tasks).select_related('from_task','to_task')
 return render(request,'studio.html',ctx(request,project=p,tasks=tasks,labels=labels,deps=deps,projects=[p] if p else [],can_edit=can_create(request.user,p)))
@login_required
def calendar(request):return render(request,'calendar.html',ctx(request,projects=(Project.objects.filter(owner=request.user)|Project.objects.filter(collaborators__user=request.user,collaborators__status='accepted')).distinct(),groups=Group.objects.filter(owner=request.user)))
