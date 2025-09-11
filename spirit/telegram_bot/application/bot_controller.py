from typing import Optional

from core.domain.services import MessageProcessor
from core.domain.value_objects import BotResponse, MessageText, UserId
from spirit.core.domain.ports import BotStatusRepository, StrategyRepository
from telegram_bot.exceptions import ProcessMessageError
from telegram_bot.infrastructure.adapters.telegram import TelegramBotAdapter
from telegram_bot.infrastructure.repositories.django import (
    DjangoBotStatusRepository,
    DjangoStrategyRepository,
)
from telegram_bot.models import BotStatusModel


class BotController:
    """Controller for managing bot lifecycle"""

    _instance: Optional["BotController"] = None

    def __init__(
        self,
        strategy_repo: Optional[StrategyRepository] = None,
        status_repo: Optional[BotStatusRepository] = None,
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
        self.adapter: Optional[TelegramBotAdapter] = None

    @classmethod
    def get_instance(cls) -> "BotController":
        """
        Возвращает единственный экземпляр контроллера (Singleton pattern)
        Эта реализация безопасна для использования в многопоточной среде
        """
        if cls._instance is None:
            # Создаем экземпляр только один раз
            cls._instance = cls()
        return cls._instance

    def is_running(self) -> bool:
        """Checks if the bot is running"""
        return self._is_running and self.status_repo.get_status()

    def process_message(
        self,
        user_id: int,
        text: str,
    ) -> BotResponse:
        """Processes incoming message"""
        try:
            return self.message_processor.process(
                UserId(user_id),
                MessageText(text),
            )
        except ProcessMessageError as e:
            return BotResponse(
                f"Processing error: {e!s}",
                requires_echo=True,
            )

    async def start(self, token: str) -> None:
        """Starts the bot"""
        if self.is_running():
            return

        # Update status in DB
        status = BotStatusModel.load()
        status.is_running = True
        status.save()

        # Start the bot
        self._is_running = True
        self.adapter = TelegramBotAdapter(token, self)
        await self.adapter.start()

    async def stop(self) -> None:
        """Stops the bot"""
        if not self.is_running():
            return

        # Update status in DB
        status = BotStatusModel.load()
        status.is_running = False
        status.save()

        # Stop the bot
        if self.adapter:
            await self.adapter.stop()
        self._is_running = False


# Константы для ошибок
BOT_CONTROLLER_NOT_SINGLETON_ERROR = (
    "BotController is a singleton. "
    "Use BotController.get_instance() to get the instance."
)
