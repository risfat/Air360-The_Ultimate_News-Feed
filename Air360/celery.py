from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from html5lib.treeadapters.sax import namespace

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Air360.settings')
app = Celery('Air360')
# app.conf.enable_utc = False

app.conf.update(timezone='Asia/Dhaka')
app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
# app.conf.beat_schedule = {
#     'send-mail-every-day-at-10': {
#         'task': 'mailer.tasks.send_mail_func',
#         'schedule': crontab(hour=9, minute=45),
#         # 'args': (2,)
#     }
#
# }

# Celery Schedules - https://docs.celeryproject.org/en/stable/reference/celery.schedules.html
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
