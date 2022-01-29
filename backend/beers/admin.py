from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from .models import Beer, BeerStyle, Brewery, Hop


class BeerAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'brewery', 'style', 'percentage', 'volume_ml')


class BreweryAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'city', 'country', 'established')


class BeerStyleAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name')


class HopAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'name', 'country')


admin.site.register(Beer, BeerAdmin)
admin.site.register(Brewery, BreweryAdmin)
admin.site.register(BeerStyle, BeerStyleAdmin)
admin.site.register(Hop, HopAdmin)
