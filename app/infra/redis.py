from typing import TYPE_CHECKING

from redis.asyncio import Redis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff


if TYPE_CHECKING:
    RedisClient: type = Redis[str]
else:
    RedisClient = Redis


def get_redis_client() -> RedisClient:
    return RedisClient.from_url(
        url='localhost',
        decode_responses=True,
        retry=Retry(ExponentialBackoff(), 10),
        retry_on_timeout=True,
    )
