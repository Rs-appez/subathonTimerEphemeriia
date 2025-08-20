from django.contrib import admin

from .models import Whell, Entry


class EntryInline(admin.TabularInline):
    model = Entry
    extra = 5


class WhellAdmin(admin.ModelAdmin):
    inlines = [EntryInline]
    save_as = True


admin.site.register(Whell, WhellAdmin)
admin.site.register(Entry)
