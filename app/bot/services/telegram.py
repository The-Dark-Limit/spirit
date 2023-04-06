import os
from typing import NoReturn

from aiogram import Bot, Dispatcher, types

from app.model.sevices.dialogpt import DialogGPT

API_TOKEN = os.getenv("BOT_TOKEN", None)
BOT = Bot(token=API_TOKEN)
DP = Dispatcher(BOT)


@DP.message_handler()
async def handle_message(message: types.Message) -> NoReturn:
    if '@big_balls_bot' in message.text:
        await get_answer(message)
    elif (
        message.reply_to_message is not None
        and message.reply_to_message.from_user['username'] == 'big_balls_bot'
    ):
        await get_answer(message)
    else:
        print(message.text)


async def get_answer(message: types.Message) -> NoReturn:
    model: DialogGPT = DialogGPT()
    uid = await model.put_request(message.text.replace('@big_balls_bot ', ''))
    result = await model.get_response(uid)
    await message.reply(result)


@DP.message_handler(commands=["start", "help"])
async def start(message: types.Message) -> NoReturn:
    await message.reply("Твой отец тебя бросил...")
