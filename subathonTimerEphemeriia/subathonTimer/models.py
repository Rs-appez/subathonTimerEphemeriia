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
    goal_name = models.CharField(max_length=100)
    goal_amount = models.FloatField()
    goal_image = models.ImageField(upload_to='subathonTimerEphemeriia/static/subathonTimer/images/tips/')

    def __str__(self):
        return self.goal_name
    
    def get_image(self):
        return self.goal_image.url[32:]
class SubGoal(models.Model):
    goal_name = models.CharField(max_length=100)
    goal_amount = models.FloatField()
    goal_image = models.ImageField(upload_to='subathonTimerEphemeriia/static/subathonTimer/images/subs/')

    def __str__(self):
        return self.goal_name
    
    def get_image(self):
        return self.goal_image.url[32:]


class Timer(models.Model):
    # Timer settings
    timer_name = models.CharField(max_length=100)
    timer_initial_time = models.IntegerField()
    timer_start = models.DateTimeField()
    timer_end = models.DateTimeField()
    timer_active = models.BooleanField(default=False)

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
    timer_message = models.CharField(max_length=100, default="Timer is currently inactive")
    timer_goal_message = models.CharField(max_length=100, default="Timer goal has not been reached")

    #Bonus time
    bonus_times = models.ManyToManyField(BonusTime, blank=True)

    def __str__(self):
        return self.timer_name
    
    def display_time(self):
        
        return self.timer_end.timestamp()
    
    def start_timer(self):
        self.timer_start = timezone.now()
        self.timer_end = self.timer_start + timezone.timedelta(seconds=self.timer_initial_time)
        self.timer_active = True
        self.save()

        write_log("Subathon started")

    def get_tip_goal(self):
        return TipGoal.objects.filter(goal_amount__gt=self.timer_total_donations).all().order_by('goal_amount')
    
    def new_sub(self, tier : int):

        self.timer_total_subscriptions += 1

        match tier:
            case 1 :
                self.timer_end += timezone.timedelta(seconds=self.timer_add_time_sub_t1)
            case 2 :
                self.timer_end += timezone.timedelta(seconds=self.timer_add_time_sub_t2)
            case 3 :
                self.timer_end += timezone.timedelta(seconds=self.timer_add_time_sub_t3)
            case _:
                return False
        self.save()

        return True
    
    def new_bits(self, bits : int):
        self.timer_total_bits += bits

        self.timer_end += timezone.timedelta(seconds=self.timer_add_time_bits * bits)

        self.save()

    def new_donation(self, donation : float):
        self.timer_total_donations += donation

        self.timer_end += timezone.timedelta(seconds=self.timer_add_time_donation * donation)

        self.save()

    def add_time(self, time : float):
        self.timer_end += timezone.timedelta(seconds=time)

        self.save()

    def add_bonus_sub(self, tier : int, multiplier : int):
        bonus_time = 0
        match tier:
            case 1 :
                bonus_time = self.timer_add_time_sub_t1
            case 2 :
                bonus_time = self.timer_add_time_sub_t2
            case 3 :
                bonus_time = self.timer_add_time_sub_t3
            case _:
                return bonus_time
            
        bonus_time *= multiplier
            
        self.timer_end += timezone.timedelta(seconds=bonus_time)
        
        self.save()

        return bonus_time
           
    def send_ticket(self):
        time = self.display_time()

        channel_layer = channels.layers.get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            settings.TICKS_GROUP_NAME,
            {
                'type': 'new_ticks',
                'content': json.dumps({'time_end': time, 'total_tips': self.timer_total_donations, 'total_subscriptions': self.timer_total_subscriptions}),
            }
        )