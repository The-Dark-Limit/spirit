from __future__ import annotations

from django.core.cache import cache
from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for Docker"""
    # Проверка базы данных
    db_conn = connections["default"]
    try:
        db_conn.cursor()
        db_status = "ok"
    except OperationalError:
        db_status = "error"

    # Проверка Redis
    try:
        cache.set("health_check", "ok", 1)
        redis_status = "ok" if cache.get("health_check") == "ok" else "error"
    except:
        redis_status = "error"

    # Проверка общего статуса
    status = "ok" if db_status == "ok" and redis_status == "ok" else "error"

    return JsonResponse({
        "status": status,
        "database": db_status,
        "redis": redis_status
    }, status=200 if status == "ok" else 500)
