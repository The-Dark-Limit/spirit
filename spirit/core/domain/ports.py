from __future__ import annotations

from abc import ABC, abstractmethod

from spirit.core.domain.strategies.base import ProcessingStrategy


class StrategyRepository(ABC):
    """Интерфейс для репозитория стратегий обработки сообщений"""

    @abstractmethod
    async def get_active_strategies(self) -> list[ProcessingStrategy]:
        """Получает все активные стратегии обработки сообщений"""


class BotStatusRepository(ABC):
    """Интерфейс для репозитория статуса бота"""

    @abstractmethod
    def get_status(self) -> bool:
        """Получает текущий статус бота (запущен/остановлен)"""


class BotOutputPort(ABC):
    """Интерфейс для адаптера вывода бота"""

    @abstractmethod
    def start(self) -> None:
        """Запускает бота"""

    @abstractmethod
    def stop(self) -> None:
        """Останавливает бота"""
