from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save

from . import signals
from .models import ResponseStrategy


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telegram_bot"
    verbose_name = "Telegram Bot"

    def ready(self):
        # Connect signals for cache invalidation
        post_save.connect(signals.invalidate_strategy_cache, sender=ResponseStrategy)
        post_delete.connect(signals.invalidate_strategy_cache, sender=ResponseStrategy)
