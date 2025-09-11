from __future__ import annotations

import os
from pathlib import Path
from typing import Any


# =============================================================================
# ОСНОВНЫЕ НАСТРОЙКИ ПРОЕКТА
# =============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Режим отладки (в production должен быть False)
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# Секретный ключ приложения (должен быть длинным и сложным)
SECRET_KEY = os.getenv("SECRET_KEY", None)
if not SECRET_KEY and not DEBUG:
    raise ValueError("SECRET_KEY must be set in production environment")

# Разрешенные хосты (для production обязательно укажите домены)
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",  # Разрешает все IPv4-адреса
    "web",  # Имя сервиса в Docker Compose
    ".localhost",  # Поддомены localhost
    "spirit_web"  # Имя контейнера
]

# Доверенные источники для CSRF (для production)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://*.yourdomain.com"  # Раскомментируйте для production
]

# Временная зона приложения
TIME_ZONE = "Europe/Moscow"

# Язык интерфейса
LANGUAGE_CODE = "ru-ru"

# Использование интернационализации
USE_I18N = True

# Использование локализованных форматов
USE_L10N = True

# Использование часовых поясов
USE_TZ = True

# URL для активации поддержки временных зон
USE_TZ = True

# =============================================================================
# НАСТРОЙКИ ПРИЛОЖЕНИЙ
# =============================================================================
INSTALLED_APPS = [
    # Стандартные приложения Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Ваши приложения
    "spirit.core",
    "spirit.telegram_bot",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "spirit.settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "spirit.settings.wsgi.application"
ASGI_APPLICATION = "spirit.settings.asgi.application"

# =============================================================================
# НАСТРОЙКИ БАЗЫ ДАННЫХ
# =============================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "spirit"),
        "USER": os.getenv("POSTGRES_USER", "spirit"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "spirit"),
        "HOST": os.getenv("POSTGRES_HOST", "db"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,  # Keep database connections alive for 60 seconds
    }
}

# Настройки аутентификации
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =============================================================================
# НАСТРОЙКИ СТАТИЧЕСКИХ И МЕДИА ФАЙЛОВ
# =============================================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "spirit" / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Настройки загрузки файлов
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB

# =============================================================================
# НАСТРОЙКИ КЭШИРОВАНИЯ
# =============================================================================
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://redis:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 100,
                "timeout": 30,
            }
        },
        "KEY_PREFIX": "spirit"
    }
}

# Настройки кэширования для стратегий
TELEGRAM_STRATEGY_CACHE_TIMEOUT = int(os.getenv("TELEGRAM_STRATEGY_CACHE_TIMEOUT", 60))

# =============================================================================
# НАСТРОЙКИ TELEGRAM БОТА
# =============================================================================
# Токен Telegram бота (обязательно)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "your_telegram_bot_token")

# Имя бота (необязательно, но рекомендуется)
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "your_bot_username")

# Максимальная длина ответа от модели Vikhr (в токенах)
TELEGRAM_VIKHR_MAX_LENGTH = int(os.getenv("TELEGRAM_VIKHR_MAX_LENGTH", 512))

# Параметр температуры для генерации (0.1-1.0)
TELEGRAM_VIKHR_TEMPERATURE = float(os.getenv("TELEGRAM_VIKHR_TEMPERATURE", 0.7))

# Таймаут для запросов к Telegram API
TELEGRAM_API_TIMEOUT = int(os.getenv("TELEGRAM_API_TIMEOUT", 20))

# =============================================================================
# НАСТРОЙКИ ЛОГГИРОВАНИЯ
# =============================================================================
LOGGING: dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module}:{lineno} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        },
        "spirit": {
            "handlers": ["console", "file"],
            "level": os.getenv("SPIRIT_LOG_LEVEL", "DEBUG" if DEBUG else "INFO"),
            "propagate": True,
        },
        "telegram_bot": {
            "handlers": ["console", "file"],
            "level": os.getenv("TELEGRAM_LOG_LEVEL", "DEBUG" if DEBUG else "INFO"),
            "propagate": True,
        },
    },
}

# =============================================================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ
# =============================================================================
# Автоматическое создание директорий для логов
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Настройки безопасности
if not DEBUG:
    # HTTPS настройки
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 год
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Защита от clickjacking
    X_FRAME_OPTIONS = "DENY"

    # Настройки CORS (если нужен API)
    # CORS_ALLOWED_ORIGINS = [
    #     "https://yourdomain.com",
    #     "https://www.yourdomain.com",
    # ]

    # Настройки Content Security Policy
    # SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_BROWSER_XSS_FILTER = True
    # SECURE_REFERRER_POLICY = "same-origin"
