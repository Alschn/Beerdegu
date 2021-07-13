from django.db import models


class Beer(models.Model):
    name = models.CharField(max_length=60)
    brewery = models.ForeignKey('Brewery', on_delete=models.SET_NULL, null=True, blank=True)
    style = models.ForeignKey('BeerStyle', on_delete=models.SET_NULL, null=True, blank=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
    volume_ml = models.PositiveIntegerField()
    image = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    hops = models.ManyToManyField('Hop', blank=True)


class Brewery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    established = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Breweries'


class BeerStyle(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, null=True, blank=True)


class Hop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
