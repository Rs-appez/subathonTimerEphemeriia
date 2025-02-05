from django.shortcuts import render, HttpResponseRedirect
from .models import Bingo, BingoItem, User
from .serializers import (
    BingoItemUserSerializer,
)

from math import sqrt
import bleach


def index(request):
    bingo = Bingo.objects.filter(is_active=True).last()

    user_name = request.GET.get("user")
    show_bingo = request.GET.get("show") != "false"

    if user_name:
        user_name = bleach.clean(user_name)
        user = User.objects.filter(name=user_name)
        if not user:
            return render(request, "bingo/error.html", {"message": "User not found"})
        else:
            user = user.first()

        bingo_items = user.get_bingo_items(bingo)
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

    bingo = Bingo.objects.filter(is_active=True).last()

    user = User.objects.get(name="Ephemeriia")

    bingo_items = user.get_bingo_items(bingo)
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
            request,
            "bingo/admin_detail.html",
            {"bingo": bingo, "bingo_items": bingo_items},
        )

    bingos = Bingo.objects.all()
    active_bingo = Bingo.objects.filter(is_active=True).last()

    return render(
        request, "bingo/admin.html", {"bingos": bingos, "active_bingo": active_bingo}
    )


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


def activate_bingo(request, bingo_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/bingo/admin/")

    bingo = Bingo.objects.get(id=bingo_id)
    bingo.activate_bingo()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
