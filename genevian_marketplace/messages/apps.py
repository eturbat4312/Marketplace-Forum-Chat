# messages/apps.py
from django.apps import AppConfig


class CustomMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messages"  # Must match your package name
    label = "custom_messages"  # Unique label
