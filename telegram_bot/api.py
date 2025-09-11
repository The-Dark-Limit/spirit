import asyncio
import threading

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .application.bot_controller import get_bot_controller


@csrf_exempt
@require_POST
def start_bot(request: HttpRequest) -> JsonResponse:
    """API endpoint for starting the bot"""
    try:
        controller = get_bot_controller()
        # Start in a separate thread as it's an async operation
        threading.Thread(
            target=lambda: asyncio.run(
                controller.start(request.settings.TELEGRAM_BOT_TOKEN),
            ),
        ).start()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_POST
def stop_bot(request: HttpRequest) -> JsonResponse:
    """API endpoint for stopping the bot"""
    try:
        controller = get_bot_controller()
        # Stop in a separate thread
        threading.Thread(
            target=lambda: asyncio.run(controller.stop()),
        ).start()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@csrf_exempt
@require_POST
def restart_bot(request: HttpRequest) -> JsonResponse:
    """API endpoint for restarting the bot"""
    try:
        controller = get_bot_controller()

        # Restart in a separate thread
        def restart() -> None:
            asyncio.run(controller.stop())
            asyncio.run(controller.start(request.settings.TELEGRAM_BOT_TOKEN))

        threading.Thread(target=restart).start()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
