from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from ratings.models import Rating


@admin.register(Rating)
class RatingAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'beer', 'note', 'added_by', 'room')
    list_select_related = ('added_by', 'room', 'beer')
