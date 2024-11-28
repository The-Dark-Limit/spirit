import os
from typing import Annotated, NoReturn

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aioinject import Inject, inject
from loguru import logger

from app.di import nn_container
from app.modules.neural_networks.services.llama import Llama

API_TOKEN = os.getenv('BOT_TOKEN', None)
BOT_USERNAME = os.getenv('BOT_USERNAME', None)
BOT = Bot(API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
DP = Dispatcher()


@DP.message(CommandStart())
async def start(message: types.Message) -> NoReturn:
    await message.reply('Твой отец тебя бросил...')

@DP.message()
@logger.catch(reraise=True)
async def handle_message(message: types.Message) -> NoReturn:
    logger.info(f'Message: {message.text}')
    async with nn_container.context() as ctx:
        service = await ctx.resolve(Llama)

        if message.text is not None and f'@{BOT_USERNAME}' in message.text:
            await get_answer(message=message, service=service)

        if (
            message.reply_to_message is not None
            and message.reply_to_message.from_user.is_bot is True
        ):
            await get_answer(message=message, service=service)

        if message.chat.type == 'private':
            await get_answer(message=message, service=service)


@inject
async def get_answer(
    message: types.Message,
    service: Annotated[Llama, Inject] = None,
) -> None:
    # uid = await service.put_request(message.text.replace(f'@{BOT_USERNAME} ', ''))
    result = await service.get_response(message)
    await message.reply(result)
