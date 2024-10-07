from rest_framework import serializers

from .models import Bingo, BingoItemUser

class BingoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bingo
        fields = '__all__'

class BingoItemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BingoItemUser
        fields = '__all__'