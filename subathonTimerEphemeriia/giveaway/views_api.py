from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Calendar, Cell, Reward, BaseCalendar
from .serializers import (
    CalendarSerializer,
    CellSerializer,
    RewardSerializer,
)

import bleach


class CalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAdminUser],
        url_path="create",
    )
    def create_calendar(self, request):
        title = bleach.clean(request.data.get("title"))
        base_calendar_id = request.data.get("base_calendar_id")
        background_url = bleach.clean(request.data.get("background_url"))

        baseCalendar = BaseCalendar.objects.get(id=base_calendar_id)
        if not baseCalendar:
            return Response({"status": "BaseCalendar not found"}, status=404)

        calendar = Calendar.objects.create(
            title=title, background_url=background_url, base_calendar=baseCalendar
        )
        calendar.generate_cells()

        serializer = CalendarSerializer(calendar)

        return Response({"status": "calendar created", "calendar": serializer.data})


class CellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Cell.objects.all()
    serializer_class = CellSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAdminUser])
    def open_cell(self, request, pk=None):
        cell = self.get_object()
        cell.open()
        return Response({"status": "cell opened", "cell": CellSerializer(cell).data})


class RewardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
