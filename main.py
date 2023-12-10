import asyncio

from app.di.containers import ServicesContainer
from app.modules.bot.telegram import DP, BOT


async def main():
    await DP.start_polling(BOT)


if __name__ == '__main__':
    container = ServicesContainer()
    container.wire(modules=[__name__, 'app.modules.bot.telegram'])
    asyncio.run(main())
