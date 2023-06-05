import asyncio

from aiogram.utils import executor
from loguru import logger

from app.bot.services.telegram import DP
from app.model.sevices.dialogpt import DialogGPT


async def do_nothing():
    logger.info('Im just do nothing, so what?')


async def on_startup(dp):
    model = DialogGPT()
    model_task = asyncio.create_task(model.serve())
    model_task.add_done_callback(do_nothing)


if __name__ == "__main__":
    executor.start_polling(DP, skip_updates=False, on_startup=on_startup)
