from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectar.settings')

app = Celery('proj')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'scrape_upbit',
        'schedule': 60.0,
        'args': ()
        },
    'scrape-daum-ticker-at-8': {
        'task': 'stock-ticker',
        'schedule': crontab(minute=0, hour=0, day_of_week='sun-thu'),
        'args': ()
        },
    'scrape-daum-kospi-info-at-9to4': {
        'task': 'kospistock-info',
        'schedule': crontab(minute='*/1', hour='0-6', day_of_week='mon-fri'),
        'args': ()
        },
    'scrape-daum-kosdaq-info-at-9to4': {
        'task': 'kosdaqstock-info',
        'schedule': crontab(minute='*/1', hour='0-6', day_of_week='mon-fri'),
        'args': ()
        },
    'get-ohlcv-01': {
        'task': 'ohlcv-get-01',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-02': {
        'task': 'ohlcv-get-02',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-03': {
        'task': 'ohlcv-get-03',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-04': {
        'task': 'ohlcv-get-04',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-05': {
        'task': 'ohlcv-get-05',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-06': {
        'task': 'ohlcv-get-06',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-07': {
        'task': 'ohlcv-get-07',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-08': {
        'task': 'ohlcv-get-08',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-09': {
        'task': 'ohlcv-get-09',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-ohlcv-10': {
        'task': 'ohlcv-get-10',
        'schedule': crontab(minute=0, hour=7, day_of_week='sun-thu'),
        'args': ()
        },
    'get-info-01': {
        'task': 'info-get-01',
        'schedule': 100,
        'args': ()
        },
    'get-info-02': {
        'task': 'info-get-02',
        'schedule': 100,
        'args': ()
        },
    'get-info-03': {
        'task': 'info-get-03',
        'schedule': 100,
        'args': ()
        },
    'get-info-04': {
        'task': 'info-get-04',
        'schedule': 100,
        'args': ()
        },
    'get-info-05': {
        'task': 'info-get-05',
        'schedule': 100,
        'args': ()
        },
    }
app.conf.timezone = 'Asia/Seoul'



# crontab(minute='*/2', hour='0-7', day_of_week='mon-fri'),
# crontab(minute='*/2', hour='0-7', day_of_week='mon-fri'),

    # 'scrape-daum-ticker-at-9': {
    #     'task': 'stock-ticker',
    #     'schedule': crontab(hour=7, day_of_week='sun-thu'),
    #     'args': ()
    #     },
    # 'scrape-daum-kospi-info-at-9to4': {
    #     'task': 'ohlcv-get',
    #     'schedule': crontab(minute='*/2', hour='0-7', day_of_week='mon-fri'),
    #     'args': ()
    #     },
    # 'scrape-daum-kosdaq-info-at-9to4': {
    #     'task': 'ohlcv-get-01',
    #     'schedule': crontab(minute='*/2', hour='0-7', day_of_week='mon-fri'),
    #     'args': ()
    #     },
