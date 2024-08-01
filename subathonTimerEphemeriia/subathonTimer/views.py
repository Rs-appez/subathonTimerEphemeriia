from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated , IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Timer
from .serializers import TimerSerializer


def index(request):
    timer = Timer.objects.get(id=1)
    time = timer.display_time()
    return render(request, 'index.html', {'time': time})


class TimerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer

    @action(detail=True, methods=['get'], permission_classes=[])
    def get_timer_info(self, request, pk=None):
        timer = self.get_object()
        time = timer.display_time()
        return Response({'time': time})
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def test(self, request, pk=None):

        timer = Timer.objects.get(id=1)
        print(timer.timer_end)
        timer.new_t3()
        print(timer.timer_end)
        timer.send_ticket()



        return Response({'message': 'This is a test'})