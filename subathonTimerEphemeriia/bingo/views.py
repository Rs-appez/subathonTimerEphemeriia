from django.shortcuts import render, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Bingo, BingoItem, BingoItemUser, User
from .serializers import (
    BingoSerializer,
    BingoItemUserSerializer,
    BingoItemSerializer,
    UserSerializer,
)

from .utils import validate_jwt_token, get_twitch_access_token, send_chat_message
from jwt import ExpiredSignatureError, InvalidTokenError

import requests
from math import sqrt
import bleach
from decouple import config

import json
from django.conf import settings
from asgiref.sync import async_to_sync
import channels.layers


def index(request):
    bingo = Bingo.objects.last()

    user_name = request.GET.get("user")
    show_bingo = request.GET.get("show") != "false"

    if user_name:
        user_name = bleach.clean(user_name)
        user = User.objects.filter(name=user_name)
        if not user:
            return render(request, "bingo/error.html", {"message": "User not found"})
        else:
            user = user.first()

        bingo_items = BingoItemUser.objects.filter(user=user).order_by("id")
        bingo_lenght = sqrt(len(bingo_items))

        return render(
            request,
            "bingo/bingo.html",
            {
                "bingo": bingo,
                "bingo_items": bingo_items,
                "bingo_lenght": bingo_lenght,
                "show_bingo": show_bingo,
            },
        )

    return render(request, "bingo/error.html", {"message": "User not found"})


def admin_bingo(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/bingo/admin/")

    user = User.objects.get(name="Ephemeriia")
    bingo_items = BingoItemUser.objects.filter(user=user).order_by("id")
    bingo_lenght = sqrt(len(bingo_items))

    return render(
        request,
        "bingo/admin_bingo.html",
        {
            "bingo_items": bingo_items,
            "bingo_lenght": bingo_lenght,
            "bingo_items_data": BingoItemUserSerializer(bingo_items, many=True).data,
        },
    )


def admin(request, bingo_id=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/bingo/admin/")

    bingo = bingo_id

    if bingo:
        bingo = Bingo.objects.get(id=bingo)
        bingo_items = BingoItem.objects.filter(bingo=bingo)

        return render(
            request, "bingo/admin.html", {"bingo": bingo, "bingo_items": bingo_items}
        )

    bingos = Bingo.objects.all()

    return render(request, "bingo/admin.html", {"bingos": bingos})


def activate_item(request, bingo_id, item_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/bingo/admin/")

    bingo_item = BingoItem.objects.get(id=item_id)
    bingo_item.activate_item()

    return HttpResponseRedirect(f"/bingo/admin/{bingo_id}/")


def reset_bingo(request, bingo_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/bingo/admin/")

    bingo = Bingo.objects.get(id=bingo_id)
    bingo.reset_all_items()

    return HttpResponseRedirect(f"/bingo/admin/{bingo_id}/")


class BingoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Bingo.objects.all()
    serializer_class = BingoSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def activate(self, request, pk=None):
        old_bingos = Bingo.objects.filter(is_active=True)
        for bingo in old_bingos:
            bingo.is_active = False
            bingo.save()
        bingo = self.get_object()
        bingo.is_active = True
        bingo.save()
        return Response({"status": "Bingo activated"})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def get_bingo(self, request):
        token = request.data.get("token")
        try:
            decoded_token = validate_jwt_token(token)
            print(decoded_token)
            user_id = decoded_token.get("user_id")

            print(user_id)

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
                print(res.json())
                username = res.json()["data"][0]["login"]
                user = User.create_with_bingoIteam(
                    name=username, id_twitch=user_id, bingo=bingo
                )
            else:
                user = user.first()

            bingo_items = BingoItemUser.objects.filter(user=user).order_by("id")

            return Response(
                {"bingo_items": BingoItemUserSerializer(bingo_items, many=True).data}
            )

        except ExpiredSignatureError:
            return Response({"status": "Token has expired"}, status=400)
        except InvalidTokenError:
            return Response({"status": "Invalid token"}, status=400)

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def reset(self, request, pk=None):
        bingo = self.get_object()
        bingo.reset_all_items()
        return Response({"status": "Bingo reset"})

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def display_bingo_widget(self, request):

        user = request.data.get("user")
        show_bingo = request.data.get("show")

        user_name = bleach.clean(user)

        channel_layer = channels.layers.get_channel_layer()

        if channel_layer is None:
            return Response({"status": "Channel layer not found"}, status=400)

        async_to_sync(channel_layer.group_send)(
            settings.BINGO_GROUP_NAME,
            {
                "type": "new_ticks",
                "content": json.dumps(
                    {
                        "type": "display_bingo_widget",
                        "user": user_name,
                        "show": show_bingo,
                    }
                ),
            },
        )

        return Response({"status": "Bingo widget displayed"})


class BingoItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BingoItem.objects.all()
    serializer_class = BingoItemSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
    def activate_item(self, request, pk=None):
        bingo_item = self.get_object()

        if bingo_item.activate_item():
            return Response({"status": "Bingo item activated"})

        return Response({"status": "Bingo item deactivated"})


class BingoItemUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BingoItemUser.objects.all()
    serializer_class = BingoItemUserSerializer

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def check_item(self, request):
        token = request.data.get("token")
        try:
            decoded_token = validate_jwt_token(token)
            user_id = decoded_token.get("user_id")
            user = User.objects.filter(id_twitch=user_id).first()
            if not user:
                return Response({"status": "User not found"}, status=400)

            bingo_item_name = request.data.get("bingo_item")
            bingo_item = BingoItemUser.objects.filter(
                bingo_item__name=bingo_item_name,
                user=user,
            ).first()
            if not bingo_item:
                return Response({"status": "Bingo item not found"}, status=400)

            bingo_item.check_item()

            bingo_finished = bingo_item.check_bingo()

            if bingo_finished and not user.has_won:
                user.win()
                send_chat_message(f"{user.name} has finished the bingo!", token)

            bingo_items = BingoItemUser.objects.filter(user=user).order_by("id")

            return Response(
                {
                    "status": "Bingo item checked",
                    "bingo_items": BingoItemUserSerializer(bingo_items, many=True).data,
                    "bingo_finished": bingo_finished,
                }
            )

        except ExpiredSignatureError:
            return Response(
                {"status": "Token has expired", "bingo_items": []}, status=400
            )
        except InvalidTokenError:
            return Response({"status": "Invalid token"}, status=400)
        except Exception as e:
            return Response({"status": str(e)}, status=400)

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def check_item_admin(self, request):
        user = User.objects.filter(name="Ephemeriia").first()
        if not user:
            return Response({"status": "User not found"}, status=400)

        bingo_item_name = request.data.get("bingo_item")
        bingo_item = BingoItemUser.objects.filter(
            bingo_item__name=bingo_item_name, user=user
        ).first()
        if not bingo_item:
            return Response({"status": "Bingo item not found"}, status=400)

        bingo_item_original = BingoItem.objects.filter(name=bingo_item_name).first()
        bingo_item_original.activate_item()

        bingo_item.check_item()

        bingo_items = BingoItemUser.objects.filter(user=user).order_by("id")
        bingo_items_data = BingoItemUserSerializer(bingo_items, many=True).data

        channel_layer = channels.layers.get_channel_layer()

        if channel_layer is None:
            return Response({"status": "Channel layer not found"}, status=400)

        async_to_sync(channel_layer.group_send)(
            settings.BINGO_GROUP_NAME,
            {
                "type": "new_ticks",
                "content": json.dumps(
                    {
                        "type": "refresh",
                        "bingo_items": bingo_items_data,
                    }
                ),
            },
        )
        return Response(
            {
                "status": "Bingo item checked",
                "bingo_items": bingo_items_data,
            }
        )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def create_user(self, request):
        name = request.data.get("name")
        bingo = request.data.get("bingo")

        if not name or not bingo:
            return Response({"status": "Invalid data"}, status=400)

        res = requests.get(
            f"https://api.twitch.tv/helix/users?login={name}",
            headers={
                "Client-ID": config("TWITCH_APP_ID"),
                "Authorization": f"Bearer {get_twitch_access_token()}",
            },
        )
        id_twitch = res.json()["data"][0]["id"]

        user = User.create_with_bingoIteam(name=name, id_twitch=id_twitch, bingo=bingo)

        return Response({"status": "User created", "user": UserSerializer(user).data})

    @action(detail=False, methods=["post"], permission_classes=[IsAdminUser])
    def reset_items(self, request):
        name = request.data.get("name")
        user = User.objects.get(name=name)
        user.reset_all_items()

        return Response({"status": "Items reset"})
