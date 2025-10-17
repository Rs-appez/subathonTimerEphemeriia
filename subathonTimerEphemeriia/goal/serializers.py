from rest_framework import serializers
from .models import Campaign, Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "title", "goal", "campaign"]


class CampaignSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    target_amount = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "current_amount",
            "target_amount",
            "is_active",
            "goals",
        ]

    def get_target_amount(self, obj):
        return obj.get_max_amount()
