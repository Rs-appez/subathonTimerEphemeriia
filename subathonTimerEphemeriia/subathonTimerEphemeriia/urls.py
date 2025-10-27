from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin_django/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("oauth/", include("oauth.urls")),
    path("timer/", include("subathonTimer.urls")),
    path("bingo/", include("bingo.urls")),
    path("info/", include("administrative.urls")),
    path("giveaway/", include("giveaway.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("goal/", include("goal.urls")),
    path("levelTracker/", include("levelTrack.urls")),
]
