from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    # Можно добавить WebSocket эндпоинты для мониторинга
    re_path(r"ws/bot-status/$", consumers.BotStatusConsumer.as_asgi()),
]
