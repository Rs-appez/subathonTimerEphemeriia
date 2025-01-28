from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import error, oauth, authorizeTwich, authorizeStreamlabs, authorizeChatbot

from .views import TwitchAuthView, StreamlabsAuthView, ChatbotAuthView

router = DefaultRouter()
router.register(r"twitch", TwitchAuthView, basename="twitch")
router.register(r"streamlabs", StreamlabsAuthView, basename="streamlabs")
router.register(r"chatbot", ChatbotAuthView, basename="chatbot")

urlpatterns = [
    path("api/auth/", include(router.urls)),
    path("error", error, name="error"),
    path("twitch/authorize", authorizeTwich, name="authorizeTwich"),
    path("streamlabs/authorize", authorizeStreamlabs, name="authorizeStreamlabs"),
    path("chatbot/authorize", authorizeChatbot, name="authorizeChatbot"),
    path("", oauth, name="oauth"),
]
