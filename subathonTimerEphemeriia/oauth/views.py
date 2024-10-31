from django.shortcuts import render, redirect, HttpResponseRedirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

import requests
from decouple import config
import uuid

from .models import TwitchAuth, StreamlabsAuth
from .serializers import TwitchAuthSerializer, StreamlabsAuthSerializer


def oauth(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/oauth/")

    ta = TwitchAuth.objects.first()
    sla = StreamlabsAuth.objects.first()

    twitch_connected = False
    twitch_user = None

    sl_connected = False
    sl_user = None

    if ta:
        twitch_connected = True

        res = requests.get(
            "https://id.twitch.tv/oauth2/validate",
            headers={"Authorization": f"OAuth {ta.access_token}"},
        )

        if res.status_code == 200:
            twitch_user = res.json()["login"]
        else:
            refresh = ta.refresh()
            if refresh:
                return redirect("oauth")

    if sla:
        sl_connected = True

        res = requests.get(
            "https://streamlabs.com/api/v2.0/user",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {sla.access_token}",
            },
        )

        if res.status_code == 200:
            sl_user = res.json()["twitch"]["display_name"]

    return render(
        request,
        "oauth.html",
        {
            "twitch_connected": twitch_connected,
            "twitch_user": twitch_user,
            "sl_connected": sl_connected,
            "sl_user": sl_user,
        },
    )


def error(request):
    return render(request, "error.html")


def authorizeTwich(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/oauth/")

    if not request.session.get("oauth_state"):
        state = uuid.uuid4()
        request.session["oauth_state"] = str(state)
    else:
        state = request.session["oauth_state"]

    redirect_uri = "https://" + config("BACKEND_HOST") + "/oauth/twitch/authorize"

    if not request.GET.get("state") == str(state):
        res = requests.get(
            "https://id.twitch.tv/oauth2/authorize",
            params={
                "client_id": config("TWITCH_APP_ID"),
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": "bits:read channel:read:redemptions channel:read:subscriptions moderator:read:followers channel:read:predictions channel:manage:predictions channel:read:redemptions channel:manage:redemptions",
                "state": state,
            },
        )

        return redirect(res.url)

    else:
        request.session["oauth_state"] = None

        res = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": config("TWITCH_APP_ID"),
                "client_secret": config("TWITCH_APP_SECRET"),
                "code": request.GET.get("code"),
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            },
        )

        if res.status_code != 200:
            return redirect("error")

        TwitchAuth.objects.create(
            access_token=res.json()["access_token"],
            refresh_token=res.json()["refresh_token"],
            expires_in=res.json()["expires_in"],
            token_type=res.json()["token_type"],
            scope=res.json()["scope"],
        )

        return redirect("oauth")


def authorizeStreamlabs(request):
    redirect_uri = "https://" + config("BACKEND_HOST") + "/oauth/streamlabs/authorize"

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/oauth/")

    if request.GET.get("code"):
        res = requests.post(
            "https://streamlabs.com/api/v2.0/token",
            data={
                "grant_type": "authorization_code",
                "client_id": config("STREAMLABS_CLIENT_ID"),
                "client_secret": config("STREAMLABS_CLIENT_SECRET"),
                "redirect_uri": redirect_uri,
                "code": request.GET.get("code"),
            },
        )

        if res.status_code != 200:
            return redirect("error")

        res_st = requests.get(
            "https://streamlabs.com/api/v2.0/socket/token",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {res.json()['access_token']}",
            },
        )

        if res_st.status_code != 200:
            return redirect("error")

        StreamlabsAuth.objects.create(
            access_token=res.json()["access_token"],
            refresh_token=res.json()["refresh_token"],
            token_type=res.json()["token_type"],
            socket_token=res_st.json()["socket_token"],
        )

        return redirect("oauth")

    res = requests.get(
        "https://streamlabs.com/api/v2.0/authorize",
        params={
            "client_id": config("STREAMLABS_CLIENT_ID"),
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "donations.read socket.token",
        },
        headers={"accept": "application/json"},
    )

    return redirect(res.url)


class TwitchAuthView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TwitchAuth.objects.all()
    serializer_class = TwitchAuthSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def first(self, request, pk=None):
        ta = TwitchAuth.objects.first()
        if ta:
            serializer = self.get_serializer(ta)
            return Response(serializer.data)
        else:
            return Response({"error": "No Twitch Auth"})

    # @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    # def refresh(self, request, pk=None):
    #     ta = TwitchAuth.objects.first()
    #     refresh = ta.refresh()

    #     return Response({'refreshed': refresh})


class StreamlabsAuthView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StreamlabsAuth.objects.all()
    serializer_class = StreamlabsAuthSerializer

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def first(self, request, pk=None):
        sla = StreamlabsAuth.objects.first()
        if sla:
            serializer = self.get_serializer(sla)
            return Response(serializer.data)
        else:
            return Response({"error": "No Streamlabs Auth"})
