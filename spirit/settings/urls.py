from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bot/", include("telegram_bot.urls")),
    # Другие URL-маршруты...
]
