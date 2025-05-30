from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Reward
from .serializers import RewardSerializer


class RewardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def activate(self, request):
        id = request.data.get("id")

        if not id:
            return Response({"error": "ID is required"}, status=400)

        try:
            reward = Reward.objects.get(reward_id=id)
            reward.send_ticket()
            return Response({"status": "Ticket sent"})
        except Reward.DoesNotExist:
            return Response({"error": "Reward not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
