from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
from decouple import config
import uuid

from .models import TwitchAuth, StreamlabsAuth

state = uuid.uuid4()


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
    
    global state

    redirect_uri = "http://" + config("BACKEND_HOST") + ":8000/oauth/twitch/authorize"

    if not request.GET.get("state") == str(state):
        state = uuid.uuid4()

        res = requests.get(
            "https://id.twitch.tv/oauth2/authorize",
            params={
                "client_id": config("APP_ID"),
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": "user:read:email",
                "state": state,
            },
        )

        return redirect(res.url)

    else:
        state = None

        res = requests.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": config("APP_ID"),
                "client_secret": config("APP_SECRET"),
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

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin_django/login/?next=/oauth/")

    redirect_uri = "http://" + config("BACKEND_HOST") + ":8000/oauth/streamlabs/authorize"

    res = requests.get(
        "https://streamlabs.com/api/v2.0/authorize",
        params={
            "client_id": config("STREAMLABS_CLIENT_ID"),
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "donations.read",
        },
    )

    return redirect(res.url)
