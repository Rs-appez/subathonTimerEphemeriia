from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from .models import Campaign, Goal
from .serializers import CampaignSerializer, GoalSerializer


class CampaignViewSet(ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [DjangoModelPermissions]


class GoalViewSet(ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [DjangoModelPermissions]
