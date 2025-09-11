from __future__ import annotations

from abc import ABC, abstractmethod

from spirit.core.domain.value_objects import BotResponse, MessageText, UserId


class ProcessingStrategy(ABC):
    """Базовый класс для всех стратегий обработки сообщений"""

    @abstractmethod
    def matches(self, text: str) -> bool:
        """Проверяет, подходит ли эта стратегия для обработки сообщения"""

    @abstractmethod
    def process(
        self,
        user_id: UserId,
        text: MessageText
    ) -> BotResponse:
        """Обрабатывает сообщение и возвращает ответ"""
