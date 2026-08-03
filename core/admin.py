from django.contrib import admin
from .models import *
admin.site.register([Profile,Project,Task,SubTask,TaskDependency,StudioLabel,CalendarEvent,NotificationLog])
