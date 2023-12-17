from enum import Enum, auto
from collections.abc import Callable

import msgspec


class RandomEventType(Enum):
    MESSAGE = auto()
    STICKER = auto()
    REACTION = auto()
    VOICE = auto()
    REPLY = auto()


class Event(msgspec.Struct):
    ...


class RandomEvent(Event):
    type: RandomEventType
    message: str | Callable | None = None
    sticker: str | None = None
    reaction: str | None = None
