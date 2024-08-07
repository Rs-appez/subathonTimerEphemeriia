from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import  oauth, authorizeTwich, authorizeStreamlabs, error
from .views import TwitchAuthView, StreamlabsAuthView

router = DefaultRouter()
router.register(r'twitch', TwitchAuthView, basename='twitch')
router.register(r'streamlabs', StreamlabsAuthView, basename='streamlabs')

urlpatterns = [
    path("api/auth/", include(router.urls)),
    path('error', error, name='error'),
    path('twitch/authorize', authorizeTwich, name='authorizeTwich'),
    path('streamlabs/authorize', authorizeStreamlabs, name='authorizeStreamlabs'),
    path('', oauth, name='oauth'),

]