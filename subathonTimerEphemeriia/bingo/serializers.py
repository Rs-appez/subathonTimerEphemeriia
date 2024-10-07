from rest_framework import serializers

from .models import Bingo, BingoItemUser, BingoItem

class BingoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bingo
        fields = '__all__'

class BingoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BingoItem
        fields = ['name']

class BingoItemUserSerializer(serializers.ModelSerializer):

    bingo_item = BingoItemSerializer()
    class Meta:
        model = BingoItemUser
        fields = ['bingo_item', 'is_checked']

