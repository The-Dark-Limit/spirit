from django.db import models

from app.modules.apps.core.models import BaseModel


class Show(BaseModel):
    name: str = models.CharField(max_length=255)
    type = None
