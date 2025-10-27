from django.db import models

class LevelTracker(models.Model):
    current_level = models.IntegerField(default=1)
    target_level = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)

    def update_level(self, new_level: int):
        self.current_level = new_level
        self.save(update_fields=["current_level"])
