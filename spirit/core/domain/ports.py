from abc import ABC, abstractmethod

from core.domain.strategies.base import ProcessingStrategy
from core.domain.value_objects import BotResponse


class StrategyRepository(ABC):
    """Порт для доступа к стратегиям обработки сообщений"""

    @abstractmethod
    def get_active_strategies(self) -> list[ProcessingStrategy]:
        """Возвращает список активных стратегий обработки"""


class BotStatusRepository(ABC):
    """Порт для доступа к состоянию бота"""

    @abstractmethod
    def get_status(self) -> bool:
        """Возвращает текущий статус бота (запущен/остановлен)"""


class BotOutputPort(ABC):
    """Порт для отправки ответов через Telegram"""

    @abstractmethod
    async def send_response(self, chat_id: int, response: BotResponse) -> None:
        """Асинхронная отправка ответа пользователю"""
