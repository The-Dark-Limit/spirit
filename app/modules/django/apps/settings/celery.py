import os

from django.conf import settings

from app.modules.django.apps.settings.utils import getenv_bool

BROKER_URL = os.environ.get('BROKER_URL', settings.REDIS_HOST)
CELERY_RESULT_BACKEND = BROKER_URL

CELERY_QUEUES = (
    Queue('main', Exchange('main'), routing_key='main'),
)

CELERY_ALWAYS_EAGER = getenv_bool('CELERY_ALWAYS_EAGER', False)
CELERY_IGNORE_RESULT = True
CELERY_TRACK_STARTED = True

CELERYBEAT_SCHEDULE = {}
