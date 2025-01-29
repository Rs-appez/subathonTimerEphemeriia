from django.db import models
import requests
from decouple import config

from oauth.models import ChatbotAuth


# Create your models here.
class Bot(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    def get_token(self):
        botAuth = ChatbotAuth.objects.get(bot_name=self.name)

        if botAuth:

            res = requests.get(
                "https://id.twitch.tv/oauth2/validate",
                headers={"Authorization": f"OAuth {botAuth.access_token}"},
            )

            if res.status_code == 200:
                token = botAuth.access_token
            else:
                botAuth.refresh()
                token = ChatbotAuth.objects.get(bot_name=self.name).access_token

            return token

    def send_message(self, message):
        token = self.get_token()

        res = requests.post(
            f"https://api.twitch.tv/helix/chat/messages",
            headers={
                "Content-Type": "application/json",
                "Client-ID": config("TWITCH_APP_ID"),
                "Authorization": f"Bearer {token}",
            },
            params={
                "text": message,
                "extension_id": config("TWITCH_APP_ID"),
                "extension_version": "0.0.1",
            },
        )

        if res.status_code == 204:
            return True

        return False
