from django.db import models

from subathonTimerEphemeriia.storage_backends import RewardStorage
from utils.utils import rename_file_to_upload


class Whell(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Entry(models.Model):
    whell = models.ForeignKey(
        Whell, on_delete=models.CASCADE, related_name="entries")
    text = models.CharField(max_length=255)
    number = models.IntegerField(default=1)
    image = models.ImageField(
        storage=RewardStorage(), upload_to=rename_file_to_upload, blank=True, null=True
    )

    def __str__(self):
        return f"{self.whell.name} - {self.text}"

    class Meta:
        unique_together = ("whell", "text")
