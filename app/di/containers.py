from aioinject import Container, providers

from app.modules.neural_networks.services.dialogpt import DialogGPTNN

container = Container()
container.register(providers.Singleton(DialogGPTNN))
