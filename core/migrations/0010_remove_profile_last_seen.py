from django.db import migrations
class Migration(migrations.Migration):
    dependencies=[('core','0009_project_summary')]
    operations=[migrations.RemoveField(model_name='profile',name='last_seen')]
