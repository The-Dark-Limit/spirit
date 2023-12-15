from collections.abc import Callable

from rq import Queue

from app.infra.redis import get_redis_client


class QueueManager:
    def __init__(self):
        self.redis = get_redis_client()
        self.queue = Queue(connection=self.redis)

    def enqueue_task(self, task: Callable, *args, **kwargs):
        self.queue.enqueue(task, *args, **kwargs)
