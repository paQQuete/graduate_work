import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'aggregate_every_five_minutes': {
        'task': 'billing.tasks.aggregate_balance_for_all_users',
        'schedule': crontab(minute='*/5'),
    },
    'check_grants_every_hour': {
        'task': 'billing.tasks.check_granted_access',
        'schedule': crontab(minute=0),
    },
}