from django.db import migrations
class Migration(migrations.Migration):
 dependencies=[('core','0007_remove_tags_add_project_slug')]
 operations=[migrations.RemoveField(model_name='profile',name='telegram_chat_id'),migrations.RemoveField(model_name='profile',name='telegram_link_token'),migrations.RemoveField(model_name='task',name='reminder_enabled'),migrations.RemoveField(model_name='calendarevent',name='notify_telegram'),migrations.DeleteModel(name='NotificationLog')]
