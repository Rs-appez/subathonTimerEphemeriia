from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import Bot
from .serializers import BotSerializer


class BotViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def speak(self, request, pk=None):
        bot = self.get_object()
        message = request.data.get("message", "")
        broadcaster_id = request.data.get("broadcaster_id", "")
        if message and broadcaster_id:
            bot.send_message(message)
            return Response({"status": "Message sent"})
        else:
            return Response({"error": "No message provided"}, status=400)
