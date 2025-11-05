from rest_framework import serializers
from .models import Campaign, Goal, CampaignType, GoalIcon


class CampaignTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignType
        fields = ["name"]


class GoalIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalIcon
        fields = ["icon"]


class GoalSerializer(serializers.ModelSerializer):
    icon = GoalIconSerializer(source="goal_icon", read_only=True)

    class Meta:
        model = Goal
        fields = ["id", "title", "goal", "campaign", "indicator", "icon"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["icon"] = representation["icon"]["icon"] if representation["icon"] else None
        return representation


class CampaignSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)
    target_amount = serializers.SerializerMethodField()
    type = CampaignTypeSerializer()

    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "type",
            "current_amount",
            "target_amount",
            "is_target_hidden",
            "is_active",
            "goals",
        ]

    def get_target_amount(self, obj):
        return obj.get_max_amount()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["type"] = representation["type"]["name"] if representation["type"] else None
        return representation
