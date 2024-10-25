import json
import os
from pathlib import Path

from app.modules.django.apps.settings.utils import getenv_bool


# APPLICATION SETTINGS
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis://redis:6379/1')
APPLICATION_NAME = 'spirit'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
STAGE_NAME = os.environ.get('STAGE_NAME', 'production')

# BASE DIR
BASE_DIR = Path(__file__).parent.parent.parent.resolve()

INTERNAL_SERVICE_REQUEST_TIMEOUT = int(
    os.environ.get('INTERNAL_SERVICE_REQUEST_TIMEOUT', 40),
)

# SECURITY
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = getenv_bool('DEBUG_MODE', False)

ALLOWED_HOSTS_DEFAULT_VALUE = ['*']
try:
    ALLOWED_HOSTS_VALUE = json.loads(
        os.environ.get('ALLOWED_HOSTS', ALLOWED_HOSTS_DEFAULT_VALUE),
    )
    ALLOWED_HOSTS = ALLOWED_HOSTS_VALUE
except TypeError:
    ALLOWED_HOSTS = ALLOWED_HOSTS_DEFAULT_VALUE

USE_X_FORWARDED_HOST = getenv_bool('USE_X_FORWARDED_HOST', True)
USE_X_FORWARDED_PORT = getenv_bool('USE_X_FORWARDED_PORT', True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# APPLICATION DEFINITIONS
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local apps
    'app.modules.django.apps.core',
    'app.modules.django.apps.shows',
    # External packages
    # 'cid',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# DJANGO CORS
CORS_ALLOW_ALL_ORIGINS = getenv_bool('CORS_ORIGIN_ALLOW_ALL', True)
CORS_URLS_REGEX = r'^.*/api/(v\d|manager)/.*$'
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'is-manager',
    'return-all-platforms',
)


# DATABASE
_db_conn_max_age = os.getenv('DB_CONN_MAX_AGE', '600')
if _db_conn_max_age is not None:
    _db_conn_max_age = int(_db_conn_max_age)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'spirit'),
        'USER': os.getenv('DB_USER', 'spirit'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'spirit'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': int(os.getenv('DB_PORT', '5432')),
        'CONN_MAX_AGE': _db_conn_max_age,
        'OPTIONS': {},
    },
}
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# USER PASSWORD VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' 'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' 'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' 'NumericPasswordValidator',
    },
]

# INTERNATIONALIZATION
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'ru-RU')
LOCALE_PATHS = (BASE_DIR / 'locale',)
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
USE_I18N = True
USE_TZ = True
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/storage/')

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = []

# CACHE
_redis_socket_timeout = os.getenv('REDIS_SOCKET_TIMEOUT', None)
if _redis_socket_timeout is not None:
    _redis_socket_timeout = int(_redis_socket_timeout)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_HOST,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_TIMEOUT': _redis_socket_timeout,
        },
    },
    'local': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
}
