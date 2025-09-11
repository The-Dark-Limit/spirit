from __future__ import annotations

from spirit.core.domain.ports import StrategyRepository
from spirit.core.domain.value_objects import BotResponse, MessageText, UserId


class MessageProcessor:
    """Сервис для обработки сообщений с использованием стратегий"""

    def __init__(self, strategy_repo: StrategyRepository) -> None:
        self.strategy_repo = strategy_repo

    async def process(
        self,
        user_id: UserId,
        text: MessageText
    ) -> BotResponse:
        """Обрабатывает сообщение, используя подходящую стратегию"""
        strategies = await self.strategy_repo.get_active_strategies()

        for strategy in strategies:
            if strategy.matches(text.value):
                return strategy.process(user_id, text)

        # Если ни одна стратегия не подошла, вернуть ошибку
        return BotResponse(
            text="Извините, я не могу обработать ваш запрос",
            requires_echo=True
        )
