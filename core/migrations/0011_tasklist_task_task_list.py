from django.db import migrations,models
import django.db.models.deletion
class Migration(migrations.Migration):
 dependencies=[('core','0010_remove_profile_last_seen')]
 operations=[migrations.CreateModel(name='TaskList',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=120)),('created_at',models.DateTimeField(auto_now_add=True)),('owner',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='task_lists',to='auth.user'))],options={'unique_together':{('name','owner')}}),migrations.AddField(model_name='task',name='task_list',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='tasks',to='core.tasklist'))]
