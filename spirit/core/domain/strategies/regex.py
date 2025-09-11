from __future__ import annotations

import re

from spirit.core.domain.strategies.base import ProcessingStrategy
from spirit.core.domain.value_objects import BotResponse, MessageText, UserId


class RegexStrategy(ProcessingStrategy):
    """Стратегия обработки по регулярному выражению"""

    def __init__(self, pattern: str, response: str) -> None:
        self.pattern = pattern
        self.regex = re.compile(pattern)
        self.response = response

    def matches(self, text: str) -> bool:
        return bool(self.regex.search(text))

    def process(
        self,
        user_id: UserId,
        text: MessageText,
    ) -> BotResponse:
        match = self.regex.search(text.value)
        if not match:
            return BotResponse("Ошибка обработки", requires_echo=False)

        formatted_response = self.response.format(**match.groupdict())
        return BotResponse(
            text=formatted_response,
            requires_echo=True,
            meta={"groups": match.groupdict()},
        )
