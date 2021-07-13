from django.contrib import admin
from .models import Beer, BeerStyle, Brewery, Hop

admin.site.register([Beer, BeerStyle, Brewery, Hop])
