from abc import ABC, abstractmethod

class IUser(ABC):
    @property
    @abstractmethod
    def email(self) -> str:
        """Возвращает email пользователя."""
        pass

    @abstractmethod
    def set_password(self, password: str) -> None:
        """Устанавливает новый пароль для пользователя."""
        pass

    @abstractmethod
    def check_password(self, password: str) -> bool:
        """Проверяет, совпадает ли указанный пароль с текущим паролем пользователя."""
        pass
