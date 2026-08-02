import os
from django.apps import AppConfig
class CoreConfig(AppConfig):
    default_auto_field='django.db.models.BigAutoField'; name='core'
    def ready(self):
      if os.environ.get('RUN_MAIN') == 'true':
        try:
          from apscheduler.schedulers.background import BackgroundScheduler
          from .scheduler import scan_tasks
          scheduler=BackgroundScheduler(timezone='Asia/Tehran'); scheduler.add_job(scan_tasks,'interval',minutes=1,id='taskflow-scan',replace_existing=True); scheduler.start()
          from .telegram_bot import start_polling; start_polling()
        except Exception: pass
