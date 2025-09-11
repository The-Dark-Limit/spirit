from dataclasses import dataclass
from typing import Any, Optional

# Константы для валидации
TELEGRAM_MESSAGE_MAX_LENGTH = 4096
USER_ID_ERROR = "User ID must be positive integer"
MESSAGE_EMPTY_ERROR = "Message text cannot be empty"
MESSAGE_LENGTH_ERROR = (
    f"Message exceeds Telegram limit ({TELEGRAM_MESSAGE_MAX_LENGTH} chars)"
)


@dataclass(frozen=True)
class UserId:
    """Value Object для идентификатора пользователя"""
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError(USER_ID_ERROR)


@dataclass(frozen=True)
class MessageText:
    """Value Object для текста сообщения"""
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError(MESSAGE_EMPTY_ERROR)
        if len(self.value) > TELEGRAM_MESSAGE_MAX_LENGTH:
            raise ValueError(MESSAGE_LENGTH_ERROR)


@dataclass(frozen=True)
class BotResponse:
    """Value Object для ответа бота"""
    text: str
    requires_echo: bool = True
    meta: Optional[dict[str, Any]] = None
