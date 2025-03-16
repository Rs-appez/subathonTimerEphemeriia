from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Calendar, Cell, Reward
from .serializers import CalendarSerializer, CellSerializer, RewardSerializer

class CalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class CellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Cell.objects.all()
    serializer_class = CellSerializer

class RewardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
