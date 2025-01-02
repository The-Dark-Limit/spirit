from core.domain.entities import User
from core.domain.value_objects import Email
from core.interfaces.abstractions.user_repository import IUserRepository
from core.services.user_service import UserService

class RegisterUserUseCase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def execute(self, email: str, password: str) -> User:
        email_value_object = Email(email)
        if not email_value_object.is_valid():
            raise ValueError("Неверный формат email.")

        existing_user = await self.user_service.get_user_by_email(email_value_object.value)
        if existing_user:
            raise ValueError("Пользователь с таким email уже существует.")

        new_user = User(email=email_value_object)
        created_user = await self.user_service.create_user(new_user, password)
        return created_user
