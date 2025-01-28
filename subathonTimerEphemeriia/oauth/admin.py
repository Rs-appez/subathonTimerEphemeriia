from django.contrib import admin

from .models import TwitchAuth, StreamlabsAuth, ChatbotAuth

admin.site.register(TwitchAuth)
admin.site.register(StreamlabsAuth)
admin.site.register(ChatbotAuth)
