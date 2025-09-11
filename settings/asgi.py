import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import telegram_bot.routing  # Импортируем наш routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(telegram_bot.routing.websocket_urlpatterns),
        ),
    },
)
