from django.utils import timezone
from .models import Task,NotificationLog,CalendarEvent
from .telegram_bot import send
def notify_once(profile,obj,kind,text,objtype):
    log,created=NotificationLog.objects.get_or_create(object_id=obj.id,object_type=objtype,notification_kind=kind)
    if created: send(profile,text)
def scan_tasks():
    now=timezone.now()
    for task in Task.objects.exclude(status='done').select_related('owner'):
      old=task.display_color; new=task.refresh_color(now)
      if old!=new: task.save(update_fields=['display_color'])
      if new in ('soon','overdue'): notify_once(task.owner,task,new,f'TaskFlow: «{task.title}» '+('مهلتش نزدیک است.' if new=='soon' else 'سررسید شده است!'),'task')
    for event in CalendarEvent.objects.filter(notify_telegram=True,starts_at__lte=now+timezone.timedelta(minutes=30),starts_at__gte=now): notify_once(event.created_by,event,'meeting',f'یادآوری TaskFlow: {event.title}','event')
