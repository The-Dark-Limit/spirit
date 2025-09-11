from __future__ import annotations

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from spirit.core.domain.ports import BotOutputPort
from spirit.telegram_bot.application.bot_controller import BotController


class TelegramBotAdapter(BotOutputPort):
    def __init__(self, token: str, controller: BotController) -> None:
        self.bot = Bot(token=token)
        self.dispatcher = Dispatcher()
        self.controller = controller

    async def setup_handlers(self) -> None:
        @self.dispatcher.message(Command(commands=["start"]))
        async def start_handler(message: Message) -> None:
            if not self.controller.is_running():
                await message.answer("Бот временно отключен")
                return

            await message.answer("Привет! Я телеграм-бот.")

        @self.dispatcher.message()
        async def message_handler(message: Message) -> None:
            if not self.controller.is_running():
                return

            if message.from_user is None:
                return

            response = self.controller.process_message(
                user_id=message.from_user.id, text=message.text or ""
            )

            if response.requires_echo:
                await message.answer(response.text)

    async def start(self) -> None:
        """Запускает polling бота"""
        await self.setup_handlers()
        await self.dispatcher.start_polling(self.bot)

    async def stop(self) -> None:
        """Останавливает бота"""
        await self.dispatcher.stop_polling()
        await self.bot.session.close()
