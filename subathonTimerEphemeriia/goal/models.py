from django.db.models.expressions import F
from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=100)
    current_amount = models.FloatField(default=0.0)
    target_amount = models.FloatField(default=0.0)
    is_target_hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    type = models.ForeignKey(
        "CampaignType", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def get_max_amount(self):
        if not self.goals.exists():
            return self.target_amount
        return max(self.goals.last().goal, self.target_amount)

    def add_amount(self, amount: float):
        self.current_amount = F("current_amount") + amount

        self.save(update_fields=["current_amount"])
        self.refresh_from_db()


class Goal(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, related_name="goals"
    )
    title = models.CharField(max_length=200)
    indicator = models.CharField(max_length=100, blank=True, null=True)
    goal_icon = models.ForeignKey(
        "GoalIcon", on_delete=models.SET_NULL, null=True, blank=True
    )
    goal = models.FloatField()

    class Meta:
        ordering = ["goal"]

    def __str__(self):
        return f"{self.title} - {self.goal}"


class CampaignType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GoalIcon(models.Model):
    icon = models.CharField(max_length=200)

    def __str__(self):
        return self.icon
