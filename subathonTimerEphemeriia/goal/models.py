from django.db import models

class Campaign(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Goal(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    goal = models.FloatField()

    def __str__(self):
        return f"{self.title} - {self.goal}€"
