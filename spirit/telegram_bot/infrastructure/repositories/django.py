import asyncio
from typing import ClassVar

from django.core.cache import cache

from core.domain.strategies import KeywordStrategy, RegexStrategy
from core.domain.strategies.default import DefaultEchoStrategy
from spirit.core.domain.ports import BotStatusRepository, StrategyRepository
from telegram_bot.models import BotStatusModel, ResponseStrategy


class DjangoStrategyRepository(StrategyRepository):
    """Repository for strategies based on Django ORM"""

    STRATEGY_CLASSES: ClassVar[dict[str, type]] = {
        "keyword": KeywordStrategy,
        "regex": RegexStrategy,
    }

    def __init__(self) -> None:
        self._cache_key = "telegram_bot:strategies:active"
        self._lock = asyncio.Lock()

    async def get_active_strategies(self) -> list:
        """Gets active strategies with caching"""
        async with self._lock:
            strategies = cache.get(self._cache_key)
            if strategies is not None:
                return strategies

            # Load from DB
            strategies = []
            for strategy in ResponseStrategy.objects.filter(is_active=True).order_by(
                "-priority",
            ):
                strategy_class = self.STRATEGY_CLASSES.get(strategy.strategy_type)
                if not strategy_class:
                    continue

                params = strategy.get_strategy_params()
                strategies.append(strategy_class(**params))

            # Add default strategy at the end
            strategies.append(DefaultEchoStrategy())

            # Cache for 60 seconds
            cache.set(self._cache_key, strategies, 60)
            return strategies


class DjangoBotStatusRepository(BotStatusRepository):
    """Repository for bot status based on Django ORM"""

    def get_status(self) -> bool:
        """Gets current bot status"""
        status = BotStatusModel.load()
        return status.is_running
