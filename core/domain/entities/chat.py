from typing import Literal

import msgspec


class Chat(msgspec.Struct): # Pydantic
    id: int
    type: Literal['private', 'supergroup']
    title: str | None
    username: str | None
    first_name: str | None
    last_name: str | None

    def to_model(self):
        pass
