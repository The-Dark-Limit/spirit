import asyncio

from app.bot.services.telegram import DP, BOT
from app.model.containers import ModelsContainer


async def main():
    await DP.start_polling(BOT)


if __name__ == '__main__':
    container = ModelsContainer()
    container.wire(modules=[__name__, 'app.bot.services.telegram'])
    asyncio.run(main())
