import asyncio

from aiogram import types

from app.modules.bot.services.telegram import DP, BOT, TelegramBotService


@DP.message()
async def handle_message(message: types.Message) -> None:
    tg_bot = TelegramBotService()
    await tg_bot.process_message(message)


async def main():
    await DP.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
