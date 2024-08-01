from django.contrib import admin

from .models import Timer, BonusTime
# Register your models here.

admin.site.register(Timer)
admin.site.register(BonusTime)