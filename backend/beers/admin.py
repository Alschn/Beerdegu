from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Beer, BeerStyle, Brewery, Hop


class BeerAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'brewery', 'style', 'percentage', 'volume_ml')
    list_select_related = ('brewery', 'style')
    search_fields = ('name', 'brewery__name', 'style__name')


class BreweryAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'city', 'country', 'established')
    search_fields = ('name', 'city')


class BeerStyleAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class HopAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'country')
    search_fields = ('name',)


admin.site.register(Beer, BeerAdmin)
admin.site.register(Brewery, BreweryAdmin)
admin.site.register(BeerStyle, BeerStyleAdmin)
admin.site.register(Hop, HopAdmin)
