from django.db import models


class Reward(models.Model):
    reward_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
