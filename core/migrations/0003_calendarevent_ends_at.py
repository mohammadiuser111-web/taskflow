from django.db import migrations, models
class Migration(migrations.Migration):
    dependencies=[('core','0002_group_project_group_calendarevent_group')]
    operations=[migrations.AddField(model_name='calendarevent',name='ends_at',field=models.DateTimeField(blank=True,null=True))]
