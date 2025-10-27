from django.db.models.expressions import F
from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    current_amount = models.FloatField(default=0.0)
    target_amount = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_max_amount(self):
        if not self.goals.exists():
            return self.target_amount
        return max(self.goals.last().goal, self.target_amount)

    def add_donation(self, donation: float):
        self.current_amount = F("current_amount") + donation

        self.save(update_fields=["current_amount"])
        self.refresh_from_db()


class Goal(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=200)
    indicator = models.CharField(max_length=100, blank=True, null=True)
    goal = models.FloatField()

    class Meta:
        ordering = ["goal"]

    def __str__(self):
        return f"{self.title} - {self.goal}€"
