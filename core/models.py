from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to='avatars/',blank=True,null=True)
    bio=models.TextField(blank=True)
    github_url=models.URLField(blank=True)

class Project(models.Model):
    name=models.CharField(max_length=160); summary=models.CharField(max_length=240,blank=True); description=models.TextField(blank=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='owned_projects'); slug=models.SlugField(max_length=180,unique=True,null=True,blank=True,allow_unicode=True); status=models.CharField(max_length=12,default='active'); completed_at=models.DateTimeField(null=True,blank=True); workspace_position=models.FloatField(default=0); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class TaskList(models.Model):
    name=models.CharField(max_length=120)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='task_lists')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=('name','owner')

class Task(models.Model):
    STATUS=[('todo','برای انجام'),('in_progress','در حال انجام'),('done','انجام‌شده')]; TYPES=[('normal','عادی'),('goal','هدف')]
    title=models.CharField(max_length=220); description=models.TextField(blank=True); owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks'); project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE,related_name='tasks'); task_list=models.ForeignKey(TaskList,null=True,blank=True,on_delete=models.SET_NULL,related_name='tasks')
    status=models.CharField(max_length=16,choices=STATUS,default='todo'); display_color=models.CharField(max_length=16,default='todo',db_index=True); due_date=models.DateTimeField(null=True,blank=True); started_at=models.DateTimeField(null=True,blank=True); task_type=models.CharField(max_length=12,choices=TYPES,default='normal'); position_x=models.FloatField(null=True,blank=True); workspace_position=models.FloatField(default=0); extension_due_date=models.DateTimeField(null=True,blank=True); position_y=models.FloatField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    def get_status_color(self,now=None):
        now=now or timezone.now()
        if self.status=='done': return 'done'
        if self.due_date and now>self.due_date:
            if self.extension_due_date and now<=self.extension_due_date: return 'soon'
            return 'overdue'
        if self.due_date and now>=self.due_date-timedelta(hours=24): return 'soon'
        return 'progress' if self.status=='in_progress' else 'todo'
    def refresh_color(self,now=None): self.display_color=self.get_status_color(now); return self.display_color
    def __str__(self): return self.title
class SubTask(models.Model):
    task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='subtasks'); title=models.CharField(max_length=220); is_done=models.BooleanField(default=False); order=models.PositiveIntegerField(default=0)
class TaskDependency(models.Model):
    from_task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='outgoing_dependencies'); to_task=models.ForeignKey(Task,on_delete=models.CASCADE,related_name='incoming_dependencies'); rule=models.CharField(max_length=20,default='blocking')
    class Meta: unique_together=('from_task','to_task')
class StudioLabel(models.Model):
    project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE,related_name='studio_labels'); owner=models.ForeignKey(User,on_delete=models.CASCADE); text=models.CharField(max_length=160); position_x=models.FloatField(default=100); position_y=models.FloatField(default=100)
class CalendarEvent(models.Model):
    TYPES=[('meeting','جلسه'),('event','رویداد')]
    project=models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE,related_name='events'); title=models.CharField(max_length=200); type=models.CharField(max_length=10,choices=TYPES); starts_at=models.DateTimeField(); ends_at=models.DateTimeField(null=True,blank=True); created_by=models.ForeignKey(User,on_delete=models.CASCADE)
