from django.contrib import admin

from .models import Timer, BonusTime, TipGoal, SubGoal
# Register your models here.

admin.site.register(Timer)
admin.site.register(BonusTime)
admin.site.register(TipGoal)
admin.site.register(SubGoal)