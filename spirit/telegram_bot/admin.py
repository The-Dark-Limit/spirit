from typing import ClassVar

from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from spirit.telegram_bot.models import BotStatusModel, ResponseStrategy

# Константы
STRATEGY_PREVIEW_LENGTH = 50


@admin.register(BotStatusModel)
class BotStatusAdmin(admin.ModelAdmin):
    """Улучшенная админка для управления состоянием бота"""

    list_display: ClassVar[list[str]] = ["status_badge", "updated_at"]
    readonly_fields: ClassVar[tuple[str, ...]] = ("updated_at", "last_error")

    @admin.display(description="Status")
    def status_badge(self, obj: BotStatusModel) -> str:
        status = "RUNNING" if obj.is_running else "STOPPED"
        color = "success" if obj.is_running else "danger"
        return format_html('<span class="badge badge-{}">{}</span>', color, status)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(
        self, request: HttpRequest, obj: BotStatusModel | None = None
    ) -> bool:
        return False

    def save_model(
        self, request: HttpRequest, obj: BotStatusModel, form: ModelForm, change: bool
    ) -> None:
        obj.updated_at = timezone.now()
        super().save_model(request, obj, form, change)


class StrategyAdminBase:
    """Базовая настройка админки для стратегий"""

    list_display: ClassVar[list[str]] = [
        "name",
        "strategy_type_badge",
        "is_active",
        "priority",
        "preview",
    ]
    list_filter: ClassVar[tuple[str, ...]] = ("strategy_type", "is_active")
    search_fields: ClassVar[tuple[str, ...]] = (
        "name",
        "keyword",
        "regex_pattern",
        "response_template",
    )
    readonly_fields: ClassVar[tuple[str, ...]] = ("created_at", "updated_at")

    fieldsets: ClassVar[tuple[tuple[str | None, dict], ...]] = (
        (None, {"fields": ("name", "strategy_type", "is_active", "priority")}),
        (
            "Parameters",
            {
                "fields": (),
                "classes": ("strategy-params",),
            },
        ),
        (
            "Response template",
            {
                "fields": ("response_template",),
                "description": mark_safe(
                    "Use <code>{text}</code> for original message, "
                    "<code>{group_name}</code> for regex captured groups"
                ),
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Type")
    def strategy_type_badge(self, obj: ResponseStrategy) -> str:
        labels = {
            "keyword": ("Keyword", "info"),
            "regex": ("Regex", "warning"),
        }
        label, color = labels.get(obj.strategy_type, ("Unknown", "secondary"))
        return format_html('<span class="badge badge-{}">{}</span>', color, label)

    @admin.display(description="Response preview")
    def preview(self, obj: ResponseStrategy) -> str:
        preview_text = (
            obj.response_template[:STRATEGY_PREVIEW_LENGTH] + "..."
            if len(obj.response_template) > STRATEGY_PREVIEW_LENGTH
            else obj.response_template
        )
        return format_html('<div class="preview-box">{}</div>', preview_text)

    def get_fieldsets(
        self, request: HttpRequest, obj: ResponseStrategy | None = None
    ) -> list[tuple[str | None, dict]]:
        base_fieldsets = list(super().get_fieldsets(request, obj))

        if obj and obj.strategy_type == "keyword":
            base_fieldsets[1][1]["fields"] = ("keyword", "case_sensitive")

        elif obj and obj.strategy_type == "regex":
            base_fieldsets[1][1]["fields"] = ("regex_pattern",)

        elif obj and obj.strategy_type == "vikhr":
            # Показываем параметры LLM для Vikhr стратегии
            base_fieldsets[1][1]["fields"] = ()
            base_fieldsets[4][1]["classes"] = []  # Показываем секцию LLM Parameters

        return base_fieldsets

    def get_readonly_fields(
        self, request: HttpRequest, obj: ResponseStrategy | None = None
    ) -> list[str] | tuple[str, ...]:
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return (*readonly_fields, "strategy_type")
        return readonly_fields


@admin.register(ResponseStrategy)
class ResponseStrategyAdmin(StrategyAdminBase, admin.ModelAdmin):
    """Улучшенная админка для настройки стратегий обработки"""

    actions: ClassVar[list[str]] = ["duplicate_strategy"]

    def duplicate_strategy(
        self, request: HttpRequest, queryset: QuerySet[ResponseStrategy]
    ) -> None:
        """Duplicates selected strategies"""
        for strategy in queryset:
            strategy.pk = None
            strategy.name = f"{strategy.name} (copy)"
            strategy.save()
        self.message_user(request, f"{queryset.count()} strategies duplicated")

    duplicate_strategy.short_description = "Duplicate selected strategies"
