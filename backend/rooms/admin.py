from django.contrib import admin
from django.db.models import Avg, QuerySet, Count, Subquery, OuterRef, IntegerField, FloatField
from django.http import HttpRequest
from import_export.admin import ImportExportActionModelAdmin
from ordered_model.admin import OrderedModelAdmin

from .models import Room, Rating, UserInRoom, BeerInRoom


@admin.register(Room)
class RoomAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'host', 'slots', 'state', 'password')
    list_select_related = ('host',)
    list_filter = ('state',)
    search_fields = ('name', 'host__username')


@admin.register(Rating)
class RatingAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'beer', 'note', 'added_by', 'room')
    list_select_related = ('added_by', 'room', 'beer')


@admin.register(BeerInRoom)
class BeerInRoomAdmin(OrderedModelAdmin, ImportExportActionModelAdmin):
    list_display = (
        'id', 'room', 'beer', 'notes_count', 'average_note',
        'order', 'move_up_down_links'
    )
    list_select_related = ('room', 'beer')
    search_fields = ('beer__name', 'room__name')
    ordering = ('-room', 'order')

    def get_queryset(self, request: HttpRequest) -> QuerySet[BeerInRoom]:
        queryset = super().get_queryset(request)

        rating_subquery = Rating.objects.filter(
            beer=OuterRef('beer'),
            room=OuterRef('room')
        ).values('beer', 'room').annotate(
            average_note=Avg('note', output_field=FloatField()),
            notes_count=Count('note', output_field=IntegerField())
        ).values('average_note', 'notes_count')

        return queryset.annotate(
            notes_count=Subquery(rating_subquery.values('notes_count')[:1]),
            average_note=Subquery(rating_subquery.values('average_note')[:1])
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
