from core.domain.strategies.base import ProcessingStrategy
from core.domain.value_objects import BotResponse, MessageText, UserId


class KeywordStrategy(ProcessingStrategy):
    """Стратегия обработки по ключевому слову"""

    def __init__(
        self,
        keyword: str,
        response: str,
        *,
        case_sensitive: bool = False,
    ) -> None:
        self.keyword = keyword
        self.response = response
        self.case_sensitive = case_sensitive

    def matches(self, text: str) -> bool:
        if self.case_sensitive:
            return self.keyword in text
        return self.keyword.lower() in text.lower()

    def process(
        self,
        user_id: UserId,
        text: MessageText,
    ) -> BotResponse:
        return BotResponse(
            text=self.response.format(text=text.value),
            requires_echo=True,
        )
