from django.db import migrations,models
class Migration(migrations.Migration):
 dependencies=[('core','0005_remove_groups_collaboration')]
 operations=[migrations.AddField(model_name='profile',name='github_url',field=models.URLField(blank=True))]
