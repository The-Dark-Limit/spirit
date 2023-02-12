import asyncio
from typing import Coroutine

from app.core.utils import Singleton


class TaskKeeper(metaclass=Singleton):
    def __init__(self):
        self.tasks = []

    async def add_task(self, task: Coroutine):
        self.tasks.append(task)

    async def remove_task(self, task: Coroutine):
        ...

    async def keep(self):
        while True:
            await asyncio.sleep(1)
