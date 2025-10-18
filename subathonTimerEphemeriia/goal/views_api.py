from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.viewsets import ModelViewSet

from .models import Campaign, Goal
from .realtime import (
    update_campaign as send_campaign_update,
    update_progress as send_progress_update,
)
from .serializers import CampaignSerializer, GoalSerializer


class CampaignViewSet(ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [DjangoModelPermissions]

    @action(detail=True, methods=["get"])
    def update_campaign(self, request, pk=None):
        campaign = self.get_object()
        send_campaign_update(campaign)
        return Response({"message": "Campaign update sent.", "status": 200})

    @action(detail=True, methods=["post"])
    def update_progress(self, request, pk=None):
        campaign: Campaign = self.get_object()
        amount = request.data.get("amount")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return Response({"message": "Invalid amount.", "status": 400})

        campaign.add_donation(amount)

        send_progress_update(campaign)
        return Response({"message": "Progress update sent.", "status": 200})


class GoalViewSet(ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [DjangoModelPermissions]
