from .models import Timer, TipGoal
from rest_framework import serializers

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = '__all__'

class TipGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipGoal
        fields = '__all__'