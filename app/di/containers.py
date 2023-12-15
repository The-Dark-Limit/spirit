from aioinject import Container, providers, Singleton

from app.modules.model.dialogpt import DialogGPTService

container = Container()
container.register(providers.Singleton(DialogGPTService))
