from dependency_injector import containers, providers

from app.model.dialogpt import DialogGPT


class ModelsContainer(containers.DeclarativeContainer):
    model_service = providers.Factory(
        DialogGPT,
    )
