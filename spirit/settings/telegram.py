from __future__ import annotations

import os


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "your_bot_username")
TELEGRAM_STRATEGY_CACHE_TIMEOUT = 60  # 60 seconds
