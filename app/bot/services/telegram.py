import os
from typing import NoReturn

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dependency_injector.wiring import Provide, inject
from loguru import logger

from app.model.containers import ModelsContainer
from app.model.dialogpt import DialogGPT

API_TOKEN = os.getenv('BOT_TOKEN', None)
BOT_USERNAME = os.getenv('BOT_USERNAME', None)
BOT = Bot(API_TOKEN, parse_mode=ParseMode.HTML)
DP = Dispatcher()

@DP.message(CommandStart())
async def start(message: types.Message) -> NoReturn:
    await message.reply('Твой отец тебя бросил...')


@DP.message()
async def handle_message(message: types.Message) -> NoReturn:
    logger.info(f'Message: {message.text}')

    if f'@{BOT_USERNAME}' in message.text:
        await get_answer(message)

    if message.reply_to_message is not None and message.reply_to_message.from_user['username'] == BOT_USERNAME:
        await get_answer(message)

    if message.chat.type == 'private':
        await get_answer(message)


@inject
async def get_answer(message: types.Message, model_service: DialogGPT = Provide[ModelsContainer.model_service]) -> None:
    uid = await model_service.put_request(message.text.replace(f'@{BOT_USERNAME} ', ''))
    result = await model_service.get_response(uid)
    await message.reply(result)
