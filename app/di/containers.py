from dependency_injector import containers, providers

from app.modules.model.dialogpt import DialogGPT


class ServicesContainer(containers.DeclarativeContainer):
    model_service = providers.Singleton(
        DialogGPT,
    )
