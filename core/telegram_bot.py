import os, requests, threading, time
from django.db import close_old_connections
from .models import Profile, NotificationLog
TOKEN=os.getenv('TELEGRAM_BOT_TOKEN',''); API=f'https://api.telegram.org/bot{TOKEN}' if TOKEN else ''
def send(profile,text):
    if not TOKEN or not profile.telegram_chat_id:return False
    try: requests.post(API+'/sendMessage',json={'chat_id':profile.telegram_chat_id,'text':text},timeout=8); return True
    except requests.RequestException:return False
def poll():
    if not TOKEN:return
    offset=None
    while True:
      try:
        r=requests.get(API+'/getUpdates',params={'timeout':25,'offset':offset},timeout=30).json()
        for u in r.get('result',[]):
          offset=u['update_id']+1; msg=u.get('message',{}); text=msg.get('text',''); chat=str(msg.get('chat',{}).get('id',''))
          if text.startswith('/start '):
            token=text.split(maxsplit=1)[1].strip(); p=Profile.objects.filter(telegram_link_token=token).first()
            if p: p.telegram_chat_id=chat; p.refresh_token(); send(p,'حساب TaskFlow شما با موفقیت متصل شد ✅')
      except Exception: time.sleep(5)
      close_old_connections()
def start_polling(): threading.Thread(target=poll,daemon=True,name='taskflow-telegram').start()
