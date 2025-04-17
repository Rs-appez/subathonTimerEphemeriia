from django.contrib import admin
from .models import Calendar, Cell, Reward, CalendarCell

admin.site.register(Calendar)
admin.site.register(Cell)
admin.site.register(Reward)
admin.site.register(CalendarCell)
