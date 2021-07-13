from django.contrib import admin

from .models import Room, Rating, UserInRoom, BeerInRoom

admin.site.register([Room, Rating, UserInRoom, BeerInRoom])
