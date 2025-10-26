from django.db import models

class LevelTracker(models.Model):
    current_level = models.IntegerField(default=1)
    target_level = models.IntegerField()

