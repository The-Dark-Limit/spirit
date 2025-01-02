from core.domain.entities import User
from core.interfaces.abstractions.user import IUser
from core.interfaces.implementations.django_user import DjangoUser
from core.domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> IUser:
        user = self.user_repository.find_by_id(user_id)
        return DjangoUser(user)

    def get_user_by_email(self, email: str) -> IUser:
        user = self.user_repository.find_by_email(email)
        return DjangoUser(user)

    def create_user(self, email: str, password: str) -> IUser:
        user = User(email=email)
        user.set_password(password)
        created_user = self.user_repository.create(user)
        return DjangoUser(created_user)

    def update_user(self, user: IUser) -> IUser:
        updated_user = self.user_repository.update(user)
        return DjangoUser(updated_user)

    def delete_user(self, user: IUser) -> None:
        self.user_repository.delete(user)
