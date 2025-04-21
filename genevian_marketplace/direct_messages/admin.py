from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "timestamp", "read", "content")
    list_filter = ("read", "timestamp", "sender", "receiver")
    search_fields = ("sender__username", "receiver__username", "content")
    fields = ("sender", "receiver", "content", "read")
    readonly_fields = ("timestamp",)
