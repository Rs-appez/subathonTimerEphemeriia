from django.urls import path
from .views import  oauth, authorizeTwich, authorizeStreamlabs

urlpatterns = [
    path('/', oauth, name='oauth'),
    path('/twitch/authorize', authorizeTwich, name='authorizeTwich'),
    path('/streamlabs/authorize', authorizeStreamlabs, name='authorizeStreamlabs')

]