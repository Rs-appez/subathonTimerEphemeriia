from django.db.models import F
from django.db import models
from django.utils import timezone

import json
from asgiref.sync import async_to_sync
import channels.layers
from django.conf import settings
from .utils import write_log


class BonusType(models.TextChoices):
    SUB = "SUB"
    FOLLOW = "FOLLOW"
    DONATION = "DONATION"
    BITS = "BITS"


class BonusTime(models.Model):
    bonus_condition = models.CharField(choices=BonusType.choices, max_length=10)
    bonus_value = models.IntegerField()
    bonus_time = models.IntegerField()
    bonus_used = models.BooleanField(default=False)


class TipGoal(models.Model):
    timer = models.ForeignKey("Timer", on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    goal_amount = models.FloatField()
    goal_image = models.ImageField(
        upload_to="subathonTimerEphemeriia/static/subathonTimer/images/tips/"
    )
    goal_image_validated = models.ImageField(
        upload_to="subathonTimerEphemeriia/static/subathonTimer/images/tips/validated/",
        null=True,
        blank=True,
    )
    validated = False

    def save(self, *args, **kwargs):
        if not self.goal_image_validated:
            self.goal_image_validated = self.goal_image
        super().save(*args, **kwargs)

    def __str__(self):
        return self.goal_name

    def get_image_validated(self):
        return self.goal_image_validated.url[32:]

    def get_image(self):
        return self.goal_image.url[32:]


class SubGoal(models.Model):
    timer = models.ForeignKey("Timer", on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    goal_amount = models.FloatField()
    goal_image = models.ImageField(
        upload_to="subathonTimerEphemeriia/static/subathonTimer/images/subs/"
    )
    validated = False

    def __str__(self):
        return self.goal_name

    def get_image(self):
        return self.goal_image.url[32:]


class Timer(models.Model):
    # Timer settings
    timer_name = models.CharField(max_length=100)
    timer_initial_time = models.IntegerField()
    timer_start = models.DateTimeField(null=True, blank=True)
    timer_end = models.DateTimeField(null=True, blank=True)
    paused_time = models.DateTimeField(null=True, blank=True)

    timer_active = models.BooleanField(default=False)
    timer_paused = models.BooleanField(default=False)

    # Timer stats
    timer_total_donations = models.FloatField(default=0)
    timer_total_subscriptions = models.IntegerField(default=0)
    timer_total_follows = models.IntegerField(default=0)
    timer_total_bits = models.IntegerField(default=0)

    # Timer add time
    timer_add_time_sub_t1 = models.IntegerField(default=0)
    timer_add_time_sub_t2 = models.IntegerField(default=0)
    timer_add_time_sub_t3 = models.IntegerField(default=0)
    timer_add_time_bits = models.FloatField(default=0)
    timer_add_time_donation = models.FloatField(default=0)

    # Timer messages
    timer_message = models.CharField(
        max_length=100, default="Timer is currently inactive"
    )
    timer_goal_message = models.CharField(
        max_length=100, default="Timer goal has not been reached"
    )

    # Bonus time
    bonus_times = models.ManyToManyField(BonusTime, blank=True)

    def __str__(self):
        return self.timer_name

    def display_time(self):
        if self.timer_end is None:
            return 0

        return self.timer_end.timestamp()

    def display_paused_time(self):
        if self.paused_time is None:
            return 0

        return self.paused_time.timestamp()

    def started_time(self):
        if self.timer_start is None:
            return 0

        return self.timer_start.timestamp()

    def start_timer(self):
        self.timer_start = timezone.now()
        self.timer_end = self.timer_start + timezone.timedelta(
            seconds=self.timer_initial_time
        )
        self.timer_active = True
        self.save()

        write_log("Subathon started")

        self.send_ticket_start()

    def pause_timer(self, user: str):
        if self.timer_paused:
            return False

        self.paused_time = timezone.now()
        self.timer_paused = True
        self.save()

        write_log("Subathon paused by " + user)

        return True

    def resume_timer(self, user: str):
        if self.paused_time is None:
            return False

        self.timer_end = F("timer_end") + (timezone.now() - self.paused_time)
        self.timer_paused = False
        self.paused_time = None
        self.save()
        self.refresh_from_db()

        write_log("Subathon resumed by " + user)

        return True

    def get_tip_goal(self):
        tip_goals = list(
            TipGoal.objects.filter(timer=self).all().order_by("goal_amount")
        )

        grouped_goals = [tip_goals[i : i + 3] for i in range(0, len(tip_goals), 3)]
        goals = []
        for i, goal in enumerate(grouped_goals):
            if goal[-1].goal_amount > self.timer_total_donations:
                goals = tip_goals[i * 3 :]
                break
        for goal in goals:
            if goal.goal_amount <= self.timer_total_donations:
                goal.validated = True
            else:
                break

        return goals

    def get_last_tip_goal(self):
        return TipGoal.objects.filter(timer=self).all().order_by("goal_amount").last()

    def get_sub_goal(self):
        sub_goals = list(
            SubGoal.objects.filter(timer=self).all().order_by("goal_amount")
        )
        grouped_goals = [sub_goals[i : i + 3] for i in range(0, len(sub_goals), 3)]
        goals = []
        for i, goal in enumerate(grouped_goals):
            if goal[-1].goal_amount > self.timer_total_subscriptions:
                goals = sub_goals[i * 3 :]
                break
        for goal in goals:
            if goal.goal_amount <= self.timer_total_subscriptions:
                goal.validated = True
            else:
                break

        return goals

    def new_sub(self, tier: int):
        self.timer_total_subscriptions = F("timer_total_subscriptions") + 1

        match tier:
            case 1:
                self.timer_end = F("timer_end") + timezone.timedelta(
                    seconds=self.timer_add_time_sub_t1
                )
            case 2:
                self.timer_end = F("timer_end") + timezone.timedelta(
                    seconds=self.timer_add_time_sub_t2
                )
            case 3:
                self.timer_end = F("timer_end") + timezone.timedelta(
                    seconds=self.timer_add_time_sub_t3
                )
            case _:
                return False
        self.save(update_fields=["timer_total_subscriptions", "timer_end"])
        self.refresh_from_db()

        return True

    def new_bits(self, bits: int):
        self.timer_total_bits = F("timer_total_bits") + bits

        self.timer_end = F("timer_end") + timezone.timedelta(
            seconds=self.timer_add_time_bits * bits
        )

        self.save(update_fields=["timer_total_bits", "timer_end"])
        self.refresh_from_db()

    def new_donation(self, donation: float):
        self.timer_total_donations = F("timer_total_donations") + donation

        self.timer_end = F("timer_end") + timezone.timedelta(
            seconds=self.timer_add_time_donation * donation
        )

        self.save(update_fields=["timer_total_donations", "timer_end"])
        self.refresh_from_db()

    def add_time(self, time: float):
        self.timer_end = F("timer_end") + timezone.timedelta(seconds=time)

        self.save(update_fields=["timer_end"])
        self.refresh_from_db()

    def add_bonus_sub(self, tier: int, multiplier: int):
        bonus_time = 0
        match tier:
            case 1:
                bonus_time = self.timer_add_time_sub_t1
            case 2:
                bonus_time = self.timer_add_time_sub_t2
            case 3:
                bonus_time = self.timer_add_time_sub_t3
            case _:
                return bonus_time

        bonus_time *= multiplier

        self.timer_end = F("timer_end") + timezone.timedelta(seconds=bonus_time)

        self.save(update_fields=["timer_end"])
        self.refresh_from_db()

        return bonus_time

    def send_ticket(self):
        time = self.display_time()
        paused_time = self.display_paused_time()

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.TICKS_GROUP_NAME,
            {
                "type": "new_ticks",
                "content": json.dumps(
                    {
                        "time_end": time,
                        "total_tips": self.timer_total_donations,
                        "total_subscriptions": self.timer_total_subscriptions,
                        "timer_paused": self.timer_paused,
                        "paused_time": paused_time,
                    }
                ),
            },
        )

    def send_ticket_start(self):
        time = self.started_time()
        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "global",
            {
                "type": "new_ticks",
                "content": json.dumps(
                    {
                        "time": time,
                    }
                ),
            },
        )
