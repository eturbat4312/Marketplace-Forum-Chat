# direct_messages/apps.py
from django.apps import AppConfig


class DirectMessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "direct_messages"
    label = "direct_messages"  # This label should be unique
