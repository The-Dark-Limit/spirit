from dependency_injector import containers, providers
from rq import Queue

from app.infra.redis import get_redis_client
from app.modules.model.dialogpt import DialogGPT


class ServicesContainer(containers.DeclarativeContainer):
    model_service = providers.Singleton(
        DialogGPT,
    )
    queue = providers.Factory(
        Queue,
        connection=get_redis_client()
    )
