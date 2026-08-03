from django.db import migrations,models
from django.utils.text import slugify
def fill(apps,schema):
 P=apps.get_model('core','Project')
 for p in P.objects.all(): p.slug=slugify(p.name,allow_unicode=True) or f'project-{p.id}';p.save(update_fields=['slug'])
class Migration(migrations.Migration):
 dependencies=[('core','0006_profile_github_url')]
 operations=[migrations.RemoveField(model_name='task',name='tags'),migrations.DeleteModel(name='Tag'),migrations.AddField(model_name='project',name='slug',field=models.SlugField(allow_unicode=True,blank=True,max_length=180,null=True,unique=True)),migrations.RunPython(fill,migrations.RunPython.noop)]
