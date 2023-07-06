from django.contrib import admin
from django.db.models import Avg, QuerySet, Count
from django.http import HttpRequest
from import_export.admin import ImportExportActionModelAdmin

from .models import Room, Rating, UserInRoom, BeerInRoom


@admin.register(Room)
class RoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'host', 'slots', 'state', 'password')
    list_select_related = ('host',)
    list_filter = ('state',)
    search_fields = ('name', 'host__username')


@admin.register(Rating)
class RatingAdmin(ImportExportActionModelAdmin):
    list_select_related = ('added_by',)


@admin.register(BeerInRoom)
class BeerInRoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'room', 'beer', 'notes_count', 'average_note')
    list_select_related = ('room', 'beer')
    search_fields = ('beer__name', 'room__name')

    def get_queryset(self, request: HttpRequest) -> QuerySet[BeerInRoom]:
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('ratings').annotate(
            notes_count=Count('ratings'),
            average_note=Avg('ratings__note')
        )

    def notes_count(self, obj) -> int:
        return obj.notes_count

    def average_note(self, obj) -> float | None:
        return obj.average_note


@admin.register(UserInRoom)
class UserInRoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'room', 'user', 'joined_at', 'last_active')
    list_select_related = ('room', 'user')
    search_fields = ('user__username', 'room__name')
    readonly_fields = ('joined_at', 'last_active')
