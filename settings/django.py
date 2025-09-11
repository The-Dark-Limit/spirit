import os
import sys
from pathlib import Path

# Основные пути
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))  # Добавляем корень проекта в PYTHONPATH

# Загрузка настроек Telegram
try:
    from .telegram import (
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_BOT_USERNAME,
        TELEGRAM_STRATEGY_CACHE_TIMEOUT,
    )
except ImportError:
    # Дефолтные значения для разработки
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TEST_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "test_bot")
    TELEGRAM_STRATEGY_CACHE_TIMEOUT = 60

# Добавьте приложение в INSTALLED_APPS
INSTALLED_APPS = [
    # Стандартные приложения Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Ваши приложения
    "core",  # If you have a separate core
    "telegram_bot",  # Our Telegram bot application
]

# Настройки кэширования (обязательно для стратегий)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Middleware для обработки асинхронных запросов
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Добавьте этот middleware для асинхронной работы
    "django_asgi.middleware.AsyncMiddleware",
]

# Добавьте в конец файла
ASGI_APPLICATION = "your_project.asgi.application"
