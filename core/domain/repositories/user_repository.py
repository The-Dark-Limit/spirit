from core.domain.entities import User
from core.domain.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_repository.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> User:
        return self.user_repository.find_by_email(email)

    def create_user(self, email: str, password: str) -> User:
        user = User(email=email, password=password)
        return self.user_repository.create(user)

    def update_user(self, user: User) -> User:
        return self.user_repository.update(user)

    def delete_user(self, user: User) -> None:
        self.user_repository.delete(user)
