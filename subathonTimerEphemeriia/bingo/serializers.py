from rest_framework import serializers

from .models import Bingo

class BingoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bingo
        fields = '__all__'