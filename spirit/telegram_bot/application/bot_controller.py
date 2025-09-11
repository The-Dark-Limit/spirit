from __future__ import annotations

import logging

from spirit.core.domain.ports import BotStatusRepository, StrategyRepository
from spirit.core.domain.value_objects import BotResponse, MessageText, UserId
from spirit.telegram_bot.infrastructure.adapters.telegram import (
    TelegramBotAdapter,
)
from spirit.telegram_bot.infrastructure.repositories.django import (
    DjangoBotStatusRepository,
    DjangoStrategyRepository,
)
from spirit.telegram_bot.models import BotStatusModel


# Настройка логгирования
logger = logging.getLogger(__name__)

# Константы для ошибок
BOT_CONTROLLER_NOT_SINGLETON_ERROR = (
    "BotController is a singleton. Use BotController.get_instance() "
    "to get the instance."
)


class BotController:
    """Контроллер для управления жизненным циклом бота"""

    _instance: BotController | None = None

    def __init__(
        self,
        strategy_repo: StrategyRepository | None = None,
        status_repo: BotStatusRepository | None = None
    ) -> None:
        """
        Инициализация контроллера.
        Этот конструктор не должен вызываться напрямую - используйте get_instance()
        """
        if BotController._instance is not None:
            raise RuntimeError(BOT_CONTROLLER_NOT_SINGLETON_ERROR)

        self.strategy_repo = strategy_repo or DjangoStrategyRepository()
        self.status_repo = status_repo or DjangoBotStatusRepository()
        self.message_processor = MessageProcessor(self.strategy_repo)
        self._is_running = False
        self.adapter: TelegramBotAdapter | None = None

    @classmethod
    def get_instance(cls) -> BotController:
        """
        Возвращает единственный экземпляр контроллера (паттерн Singleton)
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def is_running(self) -> bool:
        """Проверяет, запущен ли бот"""
        return self._is_running and self.status_repo.get_status()

    def process_message(
        self,
        user_id: int,
        text: str
    ) -> BotResponse:
        """Обрабатывает входящее сообщение"""
        try:
            return self.message_processor.process(
                UserId(user_id),
                MessageText(text)
            )
        except ValueError as e:
            logger.warning(f"Ошибка валидации при обработке сообщения: {e}")
            return BotResponse(
                f"Ошибка валидации: {e!s}",
                requires_echo=True
            )
        except Exception as e:
            logger.exception("Неожиданная ошибка при обработке сообщения")
            return BotResponse(
                f"Ошибка обработки: {e!s}",
                requires_echo=True
            )

    def start(self, token: str) -> None:
        """Запускает бота"""
        if self.is_running():
            return

        # Обновляем статус в БД
        status = BotStatusModel.load()
        status.is_running = True
        status.save()

        # Запускаем бота
        self._is_running = True
        self.adapter = TelegramBotAdapter(token, self)
        self.adapter.start()

    def stop(self) -> None:
        """Останавливает бота"""
        if not self.is_running():
            return

        # Обновляем статус в БД
        status = BotStatusModel.load()
        status.is_running = False
        status.save()

        # Останавливаем бота
        if self.adapter:
            self.adapter.stop()
        self._is_running = False
