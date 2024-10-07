from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Bingo, BingoItem, BingoItemUser, User
from .serializers import BingoSerializer, BingoItemUserSerializer
from .utils import validate_jwt_token, get_twitch_access_token
from jwt import ExpiredSignatureError, InvalidTokenError

import requests
from math import sqrt
import bleach
from decouple import config


def index(request):
    bingo = Bingo.objects.last()

    user_name = request.GET.get("user")
    if user_name:
        user_name = bleach.clean(user_name)
        user = User.objects.filter(name=user_name)
        if not user:
            # user = User.objects.create(name=user_name)
            return render(request, "bingo/error.html", {"message": "User not found"})


        else:
            user = user.first()

        bingo_items = BingoItemUser.objects.filter(user=user)
        bingo_lenght = sqrt(len(bingo_items))

        return render(
            request,
            "bingo/bingo.html",
            {"bingo": bingo, "bingo_items": bingo_items, "bingo_lenght": bingo_lenght},
        )

    return render(request, "bingo/error.html", {"message": "User not found"})


class BingoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Bingo.objects.all()
    serializer_class = BingoSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        bingo = self.get_object()
        bingo.is_active = True
        bingo.save()
        return Response({"status": "Bingo activated"})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def get_bingo(self, request):
        token = request.data.get("token")
        try:
            decoded_token = validate_jwt_token(token)
            user_id = decoded_token.get("user_id")

            bingo = Bingo.objects.filter(is_active=True).last()

            user = User.objects.filter(id_twitch=user_id)
            if not user:
                res = requests.get(
                    f"https://api.twitch.tv/helix/users?id={user_id}",
                    headers={
                        "Client-ID": config("TWITCH_APP_ID"),
                        "Authorization": f"Bearer {get_twitch_access_token()}",
                    },
                )
                username = res.json()["data"][0]["login"]
                user = User.create_with_bingoIteam(name=username, id_twitch=user_id, bingo=bingo)
            else:
                user = user.first()

            bingo_items = BingoItemUser.objects.filter(user=user)

            return Response(
                {"bingo_items": BingoItemUserSerializer(bingo_items, many=True).data}
            )

        except ExpiredSignatureError:
            return Response({"status": "Token has expired"}, status=400)
        except InvalidTokenError:
            return Response({"status": "Invalid token"}, status=400)
