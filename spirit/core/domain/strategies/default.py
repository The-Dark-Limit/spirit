from __future__ import annotations

from spirit.core.domain.strategies.base import ProcessingStrategy
from spirit.core.domain.value_objects import BotResponse, MessageText, UserId


class DefaultEchoStrategy(ProcessingStrategy):
    """Стратегия по умолчанию - эхо-ответ"""

    def matches(self, text: str) -> bool:
        return True

    def process(
        self,
        user_id: UserId,
        text: MessageText,
    ) -> BotResponse:
        return BotResponse(
            text=f"Вы написали: {text.value}",
            requires_echo=True,
        )
