from rest_framework import serializers
from .models import Whell, Entry


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ["id", "text", "image"]


class WhellSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = Whell
        fields = ["id", "name", "active", "entries"]
