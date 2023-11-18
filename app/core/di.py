from aioinject import Container, providers

from app.model.sevices.dialogpt import DialogGPT

container = Container()
container.register(providers.Callable(DialogGPT))
