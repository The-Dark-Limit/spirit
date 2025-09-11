from django.urls import path

from . import api, views

app_name = "telegram_bot"

urlpatterns = [
    # API endpoints
    path("api/bot/start/", api.start_bot, name="api-start-bot"),
    path("api/bot/stop/", api.stop_bot, name="api-stop-bot"),
    path("api/bot/restart/", api.restart_bot, name="api-restart-bot"),
    # Web interface
    path("bot/status/", views.bot_status, name="bot-status"),
]
