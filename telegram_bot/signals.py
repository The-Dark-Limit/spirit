from typing import Any

from django.core.cache import cache


def invalidate_strategy_cache(
    sender: Any,
    instance: Any,
    **kwargs: Any,
) -> None:
    """Инвалидация кэша стратегий при изменении в БД"""
    cache.delete("telegram_bot:strategies:active")
