import bleach
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Calendar, Cell, Reward, BaseCalendar, CalendarCell
from .serializers import (
    BaseCalendarSerializer,
    CalendarSerializer,
    CellSerializer,
    CalendarCellSerializer,
    RewardSerializer,
)


class BaseCalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BaseCalendar.objects.all()
    serializer_class = BaseCalendarSerializer


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

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def shuffle_reward(self, request, pk=None):
        calendar = self.get_object()
        calendar.shuffle_reward()
        return Response(
            {
                "status": "rewards shuffled",
                "calendar": CalendarSerializer(calendar).data,
            }
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def close_all(self, request, pk=None):
        calendar = self.get_object()
        calendar.close_all_cells()
        return Response(
            {
                "status": "all cells closed",
                "calendar": CalendarSerializer(calendar).data,
            }
        )


class CellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Cell.objects.all()
    serializer_class = CellSerializer


class CalendarCellViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CalendarCell.objects.all()
    serializer_class = CalendarCellSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAdminUser])
    def open_cell(self, request, pk=None):
        calendar_cell = self.get_object()
        calendar_cell.open()
        return Response(
            {
                "status": "cell opened",
                "cell": CalendarCellSerializer(calendar_cell).data,
            }
        )


class RewardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
