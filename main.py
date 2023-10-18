import asyncio
import sys

from loguru import logger

from app.bot.services.telegram import DP, BOT
from app.model.sevices.dialogpt import DialogGPT


async def do_nothing(*args, **kwargs):
    logger.info('Im just do nothing, so what?')
    logger.info(args)
    logger.info(kwargs)


async def on_startup(dp):
    model = DialogGPT()
    model_task = asyncio.create_task(model.serve())
    model_task.add_done_callback(do_nothing)

async def main():
    await DP.start_polling(BOT)

if __name__ == '__main__':
    asyncio.run(main())
