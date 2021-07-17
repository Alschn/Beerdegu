from django.contrib import admin

from .models import Room, Rating, UserInRoom, BeerInRoom


class UserInRoomAdmin(admin.ModelAdmin):
    readonly_fields = ('joined_at', 'last_active',)


admin.site.register([Room, Rating, BeerInRoom])
admin.site.register(UserInRoom, UserInRoomAdmin)
