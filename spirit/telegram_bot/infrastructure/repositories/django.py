import asyncio
from typing import ClassVar

from django.core.cache import cache

from spirit.core.domain.ports import BotStatusRepository, StrategyRepository
from spirit.core.domain.strategies.default import DefaultEchoStrategy
from spirit.core.domain.strategies.keyword import KeywordStrategy
from spirit.core.domain.strategies.regex import RegexStrategy
from spirit.core.domain.strategies.vikhr import VikhrStrategy
from spirit.telegram_bot.models import BotStatusModel, ResponseStrategy


class DjangoStrategyRepository(StrategyRepository):
    """Репозиторий стратегий на основе Django ORM"""

    STRATEGY_CLASSES: ClassVar[dict[str, type]] = {
        "keyword": KeywordStrategy,
        "regex": RegexStrategy,
        "vikhr": VikhrStrategy,
    }

    def __init__(self) -> None:
        self._cache_key = "telegram_bot:strategies:active"
        self._lock = asyncio.Lock()

    async def get_active_strategies(self) -> list:
        """Получает активные стратегии с кэшированием"""
        async with self._lock:
            strategies = cache.get(self._cache_key)
            if strategies is not None:
                return strategies

            # Загрузка из БД
            strategies = []
            for strategy in ResponseStrategy.objects.filter(is_active=True).order_by(
                "-priority"):
                strategy_class = self.STRATEGY_CLASSES.get(strategy.strategy_type)
                if not strategy_class:
                    continue

                params = strategy.get_strategy_params()
                strategies.append(strategy_class(**params))

            # Добавляем стратегию по умолчанию в конец
            strategies.append(DefaultEchoStrategy())

            # Кэшируем на 60 секунд
            cache.set(self._cache_key, strategies, 60)
            return strategies


class DjangoBotStatusRepository(BotStatusRepository):
    """Репозиторий статуса бота на основе Django ORM"""

    def get_status(self) -> bool:
        """Получает текущий статус бота"""
        status = BotStatusModel.load()
        return status.is_running
