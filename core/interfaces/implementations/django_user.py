from django.contrib.auth.models import User
from core.interfaces.abstractions.user import IUser

class DjangoUser(IUser):
    def __init__(self, user: User):
        self._user = user

    @property
    def email(self) -> str:
        return self._user.email

    def set_password(self, password: str) -> None:
        self._user.set_password(password)

    def check_password(self, password: str) -> bool:
        return self._user.check_password(password)
