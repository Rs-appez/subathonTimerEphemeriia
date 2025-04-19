from rest_framework import serializers

from .models import Calendar, Cell, Reward, BaseCalendar, CalendarCell


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


class CalendarCellSerializer(serializers.ModelSerializer):
    cell = CellSerializer()
    reward = RewardSerializer()

    class Meta:
        model = CalendarCell
        fields = "__all__"


class BaseCalendarSerializer(serializers.ModelSerializer):
    cells = CalendarCellSerializer(many=True)

    class Meta:
        model = BaseCalendar
        fields = "__all__"


class CalendarSerializer(serializers.ModelSerializer):
    base_calendar = BaseCalendarSerializer()

    class Meta:
        model = Calendar
        fields = "__all__"
