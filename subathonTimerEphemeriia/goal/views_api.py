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

    seen_ids = set()

    @action(detail=True, methods=["get"])
    def update_campaign(self, request, pk=None):
        campaign = self.get_object()
        send_campaign_update(campaign)
        return Response({"message": "Campaign update sent.", "status": 200})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def update_progress(self, request, pk=None):
        campaigns = Campaign.objects.filter(is_active=True)
        if not campaigns.exists():
            return Response({"message": "No active campaign.", "status": 400})

        amount = request.data.get("amount")
        id = request.data.get("id")

        if id in self.seen_ids:
            return Response({"message": "Already seen", "status": 400})
        self.seen_ids.add(id)

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return Response({"message": "Invalid amount.", "status": 400})

        for campaign in campaigns:
            campaign.add_donation(amount)
            send_progress_update(campaign)

        return Response({"message": "Progress update sent.", "status": 200})


class GoalViewSet(ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [DjangoModelPermissions]
