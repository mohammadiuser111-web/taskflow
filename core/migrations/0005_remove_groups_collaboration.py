from django.db import migrations
class Migration(migrations.Migration):
 dependencies=[('core','0004_workspace_completion_extensions')]
 operations=[migrations.RemoveField(model_name='project',name='group'),migrations.RemoveField(model_name='calendarevent',name='group'),migrations.DeleteModel(name='ProjectRole'),migrations.DeleteModel(name='ProjectCollaborator'),migrations.DeleteModel(name='Group')]
