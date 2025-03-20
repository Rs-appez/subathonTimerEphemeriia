from django.db import models


class Calendar(models.Model):
    title = models.CharField(max_length=200)
    size = models.IntegerField()

    mask_url = models.URLField()
    background_url = models.URLField()
    cells = models.ManyToManyField("Cell", related_name="cells")

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class Cell(models.Model):
    number = models.IntegerField()
    image_url = models.URLField()
    reward = models.ForeignKey("Reward", on_delete=models.CASCADE, null=True, blank=True)

    coordonates = models.CharField(max_length=200)

    def __str__(self):
        return str(self.number)


class Reward(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.URLField()

    def __str__(self):
        return str(self.name)
