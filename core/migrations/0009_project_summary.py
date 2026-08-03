from django.db import migrations,models
class Migration(migrations.Migration):
 dependencies=[('core','0008_remove_notifications')]
 operations=[migrations.AddField(model_name='project',name='summary',field=models.CharField(blank=True,max_length=240))]
