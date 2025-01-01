# import aioinject as ai
#
# from core.interfaces.implementations.django_user_repository import DjangoUserRepository
# from core.services.auth_service import AuthService
#
#
# def configure_di() -> ai.Container:
#     container = ai.Container()
#
#     container.bind(ai.T(IUserRepository), to=DjangoUserRepository)
#     container.bind(AuthService)
#
#     return container
#
#
# from aioinject import Injector
#
# @Injector.inject
# async def some_function(auth_service: AuthService):
#     await auth_service.authenticate('username', 'password')
#
#     from aioinject import Container, providers
#
#     from old.infra.utils.runtime_conf import Settings
#     from old.modules.neural_networks.services.dialogpt import DialogGPTNN
#     from old.modules.neural_networks.services.llama import Llama
#
#     nn_container = Container()
#     nn_container.register(providers.Singleton(DialogGPTNN))
#     nn_container.register(providers.Singleton(Llama))
#
#     settings_container = Container()
#     settings_container.register(providers.Singleton(Settings))
#
#
#
# from aioinject import Container, providers
#
# from old.infra.utils.runtime_conf import Settings
# from old.modules.neural_networks.services.dialogpt import DialogGPTNN
# from old.modules.neural_networks.services.llama import Llama
#
#
# nn_container = Container()
# nn_container.register(providers.Singleton(DialogGPTNN))
# nn_container.register(providers.Singleton(Llama))
#
#
# settings_container = Container()
# settings_container.register(providers.Singleton(Settings))
