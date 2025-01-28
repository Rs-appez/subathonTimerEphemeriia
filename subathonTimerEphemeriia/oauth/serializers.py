from .models import TwitchAuth, StreamlabsAuth, ChatbotAuth
from rest_framework import serializers


class TwitchAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchAuth
        fields = "__all__"


class StreamlabsAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamlabsAuth
        fields = "__all__"


class ChatbotAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotAuth
        fields = "__all__"
