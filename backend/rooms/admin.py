from django.contrib import admin
from django.db.models import Avg
from import_export.admin import ImportExportActionModelAdmin

from .models import Room, Rating, UserInRoom, BeerInRoom


@admin.register(Room)
class RoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'host', 'slots', 'state', 'password')


@admin.register(Rating)
class RatingAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(BeerInRoom)
class BeerInRoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'room', 'beer', 'average_note')

    def average_note(self, obj: BeerInRoom):
        if obj.ratings:
            return obj.ratings.aggregate(Avg('note'))['note__avg']
        return None


@admin.register(UserInRoom)
class UserInRoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'room', 'user', 'joined_at', 'last_active')
    readonly_fields = ('joined_at', 'last_active',)
