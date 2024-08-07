from .models import TwitchAuth, StreamlabsAuth
from rest_framework import serializers

class TwitchAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitchAuth
        fields = '__all__'

class StreamlabsAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = StreamlabsAuth
        fields = '__all__'
