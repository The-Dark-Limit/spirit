from __future__ import annotations

from django.apps import AppConfig


class TelegramBotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "spirit.telegram_bot"
    verbose_name = "Telegram Bot"

    def ready(self) -> None:
        ...
        # # Connect signals for cache invalidation
        # import spirit.telegram_bot.signals
        # from .models import ResponseStrategy
        #
        # from django.db.models.signals import post_save, post_delete
        #
        # post_save.connect(spirit.telegram_bot.signals.invalidate_strategy_cache, sender=ResponseStrategy)
        # post_delete.connect(spirit.telegram_bot.signals.invalidate_strategy_cache, sender=ResponseStrategy)
