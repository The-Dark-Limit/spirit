from django.core.cache import cache


def invalidate_strategy_cache() -> None:
    """Инвалидация кэша стратегий при изменении в БД"""
    cache.delete("telegram_bot:strategies:active")
