import asyncio

from app.modules.bot.telegram import DP, BOT


async def main():
    await DP.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
