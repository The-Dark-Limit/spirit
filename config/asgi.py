import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.django_settings')

app = get_asgi_application()

async def application(scope, receive, send):
    if scope["type"] == "http":
        await app(scope, receive, send)
    elif scope["type"] == "websocket":
        pass
    else:
        # Если другой тип соединения, возвращаем ошибку
        raise NotImplementedError(f"Unknown scope type {scope['type']}")

application = application
