from django.contrib import admin

from .models import TwitchAuth, StreamlabsAuth

admin.site.register(TwitchAuth)
admin.site.register(StreamlabsAuth)
