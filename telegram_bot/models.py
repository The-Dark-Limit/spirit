from typing import Any, ClassVar, Tuple

from django.db import models


class BotStatusModel(models.Model):
    """Singleton model for bot status management"""
    is_running = models.BooleanField(default=False, verbose_name="Bot is running")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last update")

    class Meta:
        verbose_name = "Bot status"
        verbose_name_plural = "Bot status"

    def __str__(self) -> str:
        return f"Bot Status: {'Running' if self.is_running else 'Stopped'}"

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.pk = 1
        super().save(*args, **kwargs)
        self.__class__.objects.filter(pk__gt=1).delete()

    @classmethod
    def load(cls) -> "BotStatusModel":
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj


class ResponseStrategy(models.Model):
    """Model for configuring message response strategies"""
    STRATEGY_TYPES: ClassVar[Tuple[Tuple[str, str], ...]] = (
        ("keyword", "Keyword-based"),
        ("regex", "Regex-based"),
    )

    name = models.CharField(max_length=255, verbose_name="Name")
    strategy_type = models.CharField(
        max_length=20,
        choices=STRATEGY_TYPES,
        verbose_name="Strategy type",
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    priority = models.IntegerField(default=0, verbose_name="Priority")

    # Keyword strategy parameters
    keyword = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Keyword",
    )
    case_sensitive = models.BooleanField(
        default=False,
        verbose_name="Case sensitive",
    )

    # Regex strategy parameters
    regex_pattern = models.CharField(
        max_length=500,
        blank=True,
        default="",
        verbose_name="Regex pattern",
    )

    # Common parameters
    response_template = models.TextField(verbose_name="Response template")

    class Meta:
        verbose_name = "Response strategy"
        verbose_name_plural = "Response strategies"
        ordering: ClassVar[list] = ["-priority"]

    def __str__(self) -> str:
        return f"{self.name} ({self.get_strategy_type_display()})"

    def get_strategy_params(self) -> dict:
        """Returns parameters in a format understandable by the strategy"""
        if self.strategy_type == "keyword":
            return {
                "keyword": self.keyword,
                "response": self.response_template,
                "case_sensitive": self.case_sensitive,
            }
        elif self.strategy_type == "regex":
            return {
                "pattern": self.regex_pattern,
                "response": self.response_template,
            }
        return {}
