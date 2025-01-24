from django.contrib import admin

from .models import Bingo, BingoItem, User, BingoItemUser

class BingoItemInline(admin.TabularInline):
    model = BingoItem
    extra = 9

class BingoAdmin(admin.ModelAdmin):
    inlines = [BingoItemInline]


admin.site.register(Bingo, BingoAdmin)
admin.site.register(User)
admin.site.register(BingoItemUser)
admin.site.register(BingoItem)
