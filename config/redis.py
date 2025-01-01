# if TYPE_CHECKING:
#     RedisClient: type = Redis[str]
# else:
#     RedisClient = Redis
#
#
# def get_redis_client() -> RedisClient:
#     return RedisClient.from_url(
#         url='localhost',
#         decode_responses=True,
#         retry=Retry(ExponentialBackoff(), 10),
#         retry_on_timeout=True,
#     )
