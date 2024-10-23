import os

from celery import Celery
from django.conf import settings
from kombu import Exchange, Queue

from app.modules.django.apps.settings.utils import getenv_bool


celery_app = Celery('spirit')

# Celery Configuration Options
CELERY_TIMEZONE = 'Asia/Vladivostok'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
BROKER_URL = CELERY_RESULT_BACKEND = os.environ.get('BROKER_URL', settings.REDIS_HOST)
CELERY_QUEUES = (Queue('main', Exchange('main'), routing_key='main'),)
CELERY_ALWAYS_EAGER = getenv_bool('CELERY_ALWAYS_EAGER', True)
CELERY_IGNORE_RESULT = getenv_bool('CELERY_IGNORE_RESULT', True)
CELERY_TRACK_STARTED = getenv_bool('CELERY_TRACK_STARTED', True)
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
CELERYBEAT_SCHEDULE = {}
