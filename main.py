import asyncio

from app.modules.bot.services.telegram import BOT, DP


async def main():
    await DP.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())
