from django.utils import timezone
from .models import Task
def scan_tasks():
    now=timezone.now()
    for task in Task.objects.exclude(status='done'):
        if task.display_color!=task.get_status_color(now):
            task.refresh_color(now);task.save(update_fields=['display_color'])
