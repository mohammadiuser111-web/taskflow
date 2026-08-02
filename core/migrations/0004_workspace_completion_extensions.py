from django.db import migrations,models
class Migration(migrations.Migration):
 dependencies=[('core','0003_calendarevent_ends_at')]
 operations=[migrations.AddField(model_name='project',name='status',field=models.CharField(default='active',max_length=12)),migrations.AddField(model_name='project',name='completed_at',field=models.DateTimeField(blank=True,null=True)),migrations.AddField(model_name='project',name='workspace_position',field=models.FloatField(default=0)),migrations.AddField(model_name='task',name='workspace_position',field=models.FloatField(default=0)),migrations.AddField(model_name='task',name='extension_due_date',field=models.DateTimeField(blank=True,null=True))]
