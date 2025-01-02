import aioinject

from core.domain.repositories.user_repository import UserService
from core.interfaces.abstractions.user import IUser
from core.interfaces.implementations.django_user import DjangoUser


def configure_di() -> aioinject.Container:
    container = aioinject.Container()

    container.bind(aioinject.T(IUser), to=DjangoUser)
    container.bind(aioinject.T(UserRepository), to=DjangoUserRepository)
    container.bind(UserService)

    return container
