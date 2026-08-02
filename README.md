# TaskFlow

یک اپ Django تک‌فرایندی برای مدیریت وظیفه، پروژه، همکاری و بوم وابستگی‌ها؛ رابط کاملاً فارسی و RTL است.

## اجرا

```bash
python -m venv venv
source venv/bin/activate              # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

برای تلگرام، `.env.example` را به `.env` کپی کنید و `TELEGRAM_BOT_TOKEN` و `TELEGRAM_BOT_USERNAME` را تنظیم کنید. بدون آن نیز همه قابلیت‌های غیرتلگرامی کار می‌کنند. زمان‌بند APScheduler و polling تلگرام در child process `runserver` آغاز می‌شوند و هیچ سرویس جانبی لازم نیست.

## امکانات

- حساب کاربری، پروفایل و اتصال امن یک‌بارمصرف تلگرام
- وظیفه، زیرکار، برچسب، پروژه و همکاری نقش‌محور
- صفحه Studio با جابه‌جایی pointer-based، اتصال SVG و جلوگیری سمت سرور از دورزدن وابستگی
- گره‌های هدف، وضعیت/رنگ محاسبه‌شده، یادآوری و مهلت‌ها
- حضور همکاران با heartbeat و تقویم ماهانه
