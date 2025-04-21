# direct_messages/views.py
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user)).order_by(
            "-timestamp"
        )

    def perform_create(self, serializer):
        # Save the message with the logged-in user as sender.
        serializer.save(sender=self.request.user)
