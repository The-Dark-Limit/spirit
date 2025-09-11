import json
from typing import Any, Dict

from channels.generic.websocket import AsyncWebsocketConsumer

from telegram_bot.models import BotStatusModel


class BotStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        await self.accept()
        await self.channel_layer.group_add("bot_status", self.channel_name)

        # Send current status on connect
        status = BotStatusModel.load()
        await self.send(
            text_data=json.dumps(
                {
                    "is_running": status.is_running,
                    "updated_at": str(status.updated_at),
                },
            ),
        )

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard("bot_status", self.channel_name)

    async def bot_status_update(self, event: Dict[str, Any]) -> None:
        await self.send(text_data=json.dumps(event))
