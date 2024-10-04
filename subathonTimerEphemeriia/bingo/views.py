from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Bingo, BingoItem, BingoItemUser, User
from .serializers import BingoSerializer

from math import sqrt
import bleach

def index(request):
    bingo = Bingo.objects.last()


    user_name = request.GET.get('user')
    if user_name:

        user_name = bleach.clean(user_name)
        user = User.objects.filter(name=user_name)
        if not user:
            user = User.objects.create(name=user_name)
            bingo_default_items = BingoItem.objects.filter(bingo=bingo).order_by('?')
            for bingo_item in bingo_default_items:
                BingoItemUser.objects.create(user=user, bingo_item=bingo_item)
            
        else:
            user = user.first()

        bingo_items = BingoItemUser.objects.filter(user=user)
        bingo_lenght = sqrt(len(bingo_items))

        return render(request, 'bingo/bingo.html', {'bingo': bingo, 'bingo_items': bingo_items, 'bingo_lenght': bingo_lenght})
    
    return  render(request, 'bingo/error.html', {'message': 'User not found'})


class BingoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Bingo.objects.all()
    serializer_class = BingoSerializer

    @action(detail=True, methods=['post'],permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        bingo = self.get_object()
        bingo.is_active = True
        bingo.save()
        return Response({'status': 'Bingo activated'})
