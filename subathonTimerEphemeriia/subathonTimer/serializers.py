from .models import Timer, TipGoal, CarouselAnnouncement
from rest_framework import serializers


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = "__all__"


class TipGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipGoal
        fields = "__all__"


class CarouselAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselAnnouncement
        fields = "__all__"
