# direct_messages/serializers.py
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)
    receiver_username = serializers.CharField(
        source="receiver.username", read_only=True
    )
    listing_link = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "sender_username",
            "receiver",
            "receiver_username",
            "content",
            "timestamp",
            "read",
            "listing",
            "listing_link",
        ]
        read_only_fields = [
            "id",
            "timestamp",
            "sender",
            "read",
            "sender_username",
            "receiver_username",
            "listing_link",
        ]

    def get_listing_link(self, obj):
        if obj.listing:
            # Return a relative URL to the listing detail page.
            return f"/listings/{obj.listing.id}/"
        return None
