from django.contrib import admin
from .models import *
admin.site.register([Profile,Project,Tag,Task,SubTask,TaskDependency,StudioLabel,ProjectCollaborator,ProjectRole,CalendarEvent,NotificationLog])
