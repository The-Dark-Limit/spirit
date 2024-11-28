from aioinject import Container, providers

from app.infra.utils.runtime_conf import Settings
from app.modules.neural_networks.services.dialogpt import DialogGPTNN
from app.modules.neural_networks.services.llama import Llama


nn_container = Container()
nn_container.register(providers.Singleton(DialogGPTNN))
nn_container.register(providers.Singleton(Llama))


settings_container = Container()
settings_container.register(providers.Singleton(Settings))
