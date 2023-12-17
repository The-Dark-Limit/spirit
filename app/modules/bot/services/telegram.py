import os
from typing import NoReturn

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from loguru import logger

from app.modules.neural_networks.services.dialogpt import DialogGPTNNService
from app.modules.neural_networks.typings import ModelServiceT
from app.modules.random_events.entity.random_events import RandomEventType
from app.modules.random_events.services.random_events import RandomEventsService
from app.modules.random_events.typings import EventServiceT, EventT

API_TOKEN = os.getenv('BOT_TOKEN', None)
BOT_USERNAME = os.getenv('BOT_USERNAME', None)
BOT = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
DP = Dispatcher()


class TelegramBotService:
    def __init__(
        self,
        event_service: EventServiceT = RandomEventsService,
        model_service: ModelServiceT = DialogGPTNNService,
    ) -> None:
        self._event_service = event_service
        self._model_service = model_service

    async def process_message(
        self,
        message: types.Message,
    ) -> NoReturn:
        logger.info(f'Message: {message.text}')
        if event := self._event_service().roll_event(2):
            logger.info('Random event!')
            await self.execute_event(message, event)

        if message.text is not None and f'@{BOT_USERNAME}' in message.text:
            await self.get_answer(message)

        if message.reply_to_message is not None and message.reply_to_message.from_user.is_bot is True:
            await self.get_answer(message)

        if message.chat.type == 'private':
            await self.get_answer(message)

    async def get_answer(
        self,
        message: types.Message,
    ) -> None:
        service = self._model_service()
        uid = await service.put_request(message.text.replace(f'@{BOT_USERNAME} ', ''))
        result = await service.get_response(uid)
        await message.reply(result)

    async def execute_event(self, message: types.Message, event: EventT) -> None:
        if event.type == RandomEventType.MESSAGE:
            await message.reply(event.message)
        if event.type == RandomEventType.STICKER:
            await message.answer_sticker(event.sticker)
        if event.type == RandomEventType.REPLY:
            await self.get_answer(message)

    @DP.message(CommandStart())
    async def start(self, message: types.Message) -> NoReturn:
        await message.reply('Твой отец тебя бросил...')
