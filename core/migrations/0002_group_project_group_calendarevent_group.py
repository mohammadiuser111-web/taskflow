from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[('core','0001_initial')]
    operations=[
        migrations.CreateModel(name='Group',fields=[
            ('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),
            ('name',models.CharField(max_length=120)),('description',models.TextField(blank=True)),('created_at',models.DateTimeField(auto_now_add=True)),
            ('owner',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='task_groups',to='auth.user')),
        ],options={'unique_together':{('name','owner')}}),
        migrations.AddField(model_name='project',name='group',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='projects',to='core.group')),
        migrations.AddField(model_name='calendarevent',name='group',field=models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.SET_NULL,related_name='events',to='core.group')),
    ]
