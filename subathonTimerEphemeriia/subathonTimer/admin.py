from django.contrib import admin

from .models import Timer, BonusTime, TipGoal, SubGoal

class GoalAdmin(admin.ModelAdmin):

    list_display = ( "goal_name",'goal_amount')

admin.site.register(Timer)
admin.site.register(BonusTime)
admin.site.register(TipGoal,GoalAdmin)
admin.site.register(SubGoal,GoalAdmin)