from abc import ABC, abstractmethod

from core.domain.value_objects import BotResponse, MessageText, UserId


class ProcessingStrategy(ABC):
    """Базовый класс для стратегий обработки сообщений"""

    @abstractmethod
    def matches(self, text: str) -> bool:
        """Проверяет, применима ли стратегия к данному тексту"""

    @abstractmethod
    def process(self, user_id: UserId, text: MessageText) -> BotResponse:
        """Обрабатывает сообщение и возвращает ответ"""
