import os

from aiogram import Bot, Dispatcher, types

from app.model.sevices.dialogpt import DialogGPT

API_TOKEN = os.getenv("BOT_TOKEN", None)
BOT = Bot(token=API_TOKEN)
DP = Dispatcher(BOT)


@DP.message_handler()
async def handle_message(message: types.Message) -> None:
    model: DialogGPT = DialogGPT()
    uid = await model.put_request(message.text)
    result = await model.get_response(uid)
    await message.reply(result)


@DP.message_handler(commands=["start", "help"])
async def start(message: types.Message) -> None:
    await message.reply("DialogGPT Bot")
