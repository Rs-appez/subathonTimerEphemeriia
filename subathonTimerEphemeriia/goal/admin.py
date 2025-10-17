from django.contrib import admin

from .models import Campaign, Goal

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    class GoalInline(admin.TabularInline):
        model = Goal
        extra = 3

    inlines = [GoalInline]
