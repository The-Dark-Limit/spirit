from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from telegram_bot.models import BotStatusModel, ResponseStrategy


@staff_member_required
def bot_status(request: HttpRequest) -> HttpResponse:
    """Страница мониторинга бота для администраторов"""
    status = BotStatusModel.load()
    strategies = list(
        ResponseStrategy.objects.filter(is_active=True).order_by("-priority"),
    )

    return render(
        request,
        "telegram_bot/status.html",
        {
            "status": status,
            "strategies": strategies,
            "active_strategies_count": len(strategies),
        },
    )
