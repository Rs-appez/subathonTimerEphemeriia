from django.contrib import admin

from .models import Timer, BonusTime, TipGoal, SubGoal, CarouselAnnouncement


class GoalAdmin(admin.ModelAdmin):
    save_as = True
    list_display = ("goal_name", "goal_amount")


admin.site.register(Timer)
admin.site.register(BonusTime)
admin.site.register(TipGoal, GoalAdmin)
admin.site.register(SubGoal, GoalAdmin)
admin.site.register(CarouselAnnouncement)
