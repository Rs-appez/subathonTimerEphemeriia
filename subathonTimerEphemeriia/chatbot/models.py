from django.db import models
import requests
from decouple import config

from oauth.models import ChatbotAuth


# Create your models here.
class Bot(models.Model):
    name = models.CharField(max_length=255)
    twitch_id = models.CharField(max_length=255)

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

    def send_message(self, message, broadcaster_id):
        token = self.get_token()

        res = requests.post(
            f"https://api.twitch.tv/helix/chat/messages",
            headers={
                "Content-Type": "application/json",
                "Client-ID": config("TWITCH_APP_ID"),
                "Authorization": f"Bearer {token}",
            },
            params={
                "message": message,
                "sender_id": self.twitch_id,
                "broadcaster_id": broadcaster_id,
            },
        )

        if res.status_code == 204:
            return True

        return False
