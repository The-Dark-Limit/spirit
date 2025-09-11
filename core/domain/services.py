
from core.domain.ports import StrategyRepository
from core.domain.strategies.default import DefaultEchoStrategy
from core.domain.value_objects import BotResponse, MessageText, UserId


class MessageProcessor:
    """Сервис обработки сообщений через стратегии"""

    def __init__(self, strategy_repo: StrategyRepository) -> None:
        self.strategy_repo = strategy_repo

    def process(self, user_id: UserId, text: MessageText) -> BotResponse:
        """Обрабатывает сообщение, применяя подходящую стратегию"""
        strategies = self.strategy_repo.get_active_strategies()

        for strategy in strategies:
            if strategy.matches(text.value):
                return strategy.process(user_id, text)

        # Если нет подходящих стратегий, используем дефолтную
        return DefaultEchoStrategy().process(user_id, text)
