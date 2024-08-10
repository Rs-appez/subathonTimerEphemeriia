from django.db import models
import requests
from decouple import config

# Create your models here.

class TwitchAuth(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    token_type = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.access_token
    
    def refresh(self):
        res = requests.post('https://id.twitch.tv/oauth2/token', params={
            'client_id': config("TWITCH_APP_ID"),
            'client_secret': config("TWITCH_APP_SECRET"),
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        })

        if res.status_code == 200:
            data = res.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.expires_in = data['expires_in']
            self.token_type = data['token_type']
            self.scope = data['scope']
            self.save()
        else:
            
            return False

        return True
    
class StreamlabsAuth(models.Model):
    access_token = models.CharField(max_length=2083)
    refresh_token = models.CharField(max_length=2083)
    socket_token = models.CharField(max_length=2083)
    token_type = models.CharField(max_length=255)
    scope = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.access_token