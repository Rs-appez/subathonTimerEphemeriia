from rest_framework import serializers

from .models import Calendar, Cell, Reward


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


class CalendarSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True)

    class Meta:
        model = Calendar
        fields = "__all__"
