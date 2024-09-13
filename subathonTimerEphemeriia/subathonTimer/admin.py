from django.contrib import admin

from .models import Timer, BonusTime, TipGoal
# Register your models here.

admin.site.register(Timer)
admin.site.register(BonusTime)
admin.site.register(TipGoal)