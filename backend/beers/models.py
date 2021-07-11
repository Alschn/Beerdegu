from django.db import models


class Beer:
    name = ''
    brewery = 'FK'
    style = 'FK'
    percentage = ''
    volume_ml = ''
    description = ''
    image = ''


class Brewery:
    name = ''
    country = ''
    description = ''


class BeerStyle:
    name = ''
    description = ''


class Hop:
    name = ''
    description = ''
    country = ''
