import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTING_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_every_week': {
        'task': 'news.tasks.every_wk_news_mailing',
        #'schedule': 30,
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        #'args': (args),

    },
}

