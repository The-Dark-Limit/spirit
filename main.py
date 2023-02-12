import asyncio
from concurrent.futures import ProcessPoolExecutor

from aiogram.utils import executor

from app.bot.services.telegram import DP
from app.core.tasks import TaskKeeper
from app.model.sevices.dialogpt import DialogGPT


async def keep_always():
    task_kepper_instance = TaskKeeper()
    task_keeper = asyncio.create_task(task_kepper_instance.keep())
    task_keeper.add_done_callback(keep_always)


async def do_nothing():
    ...


async def on_startup(dp):
    loop = asyncio.get_event_loop()
    model = DialogGPT()
    # task_kepper_instance = TaskKeeper()

    model_task = asyncio.create_task(model.serve(), name='Model Idle')
    # task_keeper = asyncio.create_task(task_kepper_instance.keep())
    model_task.add_done_callback(do_nothing)
    # task_keeper.add_done_callback(keep_always)


if __name__ == "__main__":
    executor.start_polling(DP, skip_updates=True, on_startup=on_startup)
