from django.db import models
from django.utils import timezone

import json
from asgiref.sync import async_to_sync
import channels.layers
from django.conf import settings

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

class Timer(models.Model):
    # Timer settings
    timer_name = models.CharField(max_length=100)
    timer_initial_time = models.IntegerField()
    timer_start = models.DateTimeField()
    timer_end = models.DateTimeField()
    timer_active = models.BooleanField(default=False)

    # Timer stats
    timer_total_donations = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timer_total_subscriptions = models.IntegerField(default=0)
    timer_total_follows = models.IntegerField(default=0)


    # Timer add time
    timer_add_time_sub_t1 = models.IntegerField(default=0)
    timer_add_time_sub_t2 = models.IntegerField(default=0)
    timer_add_time_sub_t3 = models.IntegerField(default=0)
    timer_add_time_bits = models.IntegerField(default=0)
    timer_add_time_donation = models.IntegerField(default=0)


    # Timer messages
    timer_message = models.CharField(max_length=100, default="Timer is currently inactive")
    timer_goal_message = models.CharField(max_length=100, default="Timer goal has not been reached")

    #Bonus time
    bonus_times = models.ManyToManyField(BonusTime, blank=True)

    def __str__(self):
        return self.timer_name
    
    def display_time(self):
        
        return self.timer_end.timestamp()
    
    def new_t3(self):
        self.timer_total_subscriptions += 1
        self.timer_end += timezone.timedelta(seconds=self.timer_add_time_sub_t3)
        self.save()

    def send_ticket(self):
        time = self.display_time()

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.TICKS_GROUP_NAME,
            {
                'type': 'new_ticks',
                'content': json.dumps({'time_end': time})
            }
        )