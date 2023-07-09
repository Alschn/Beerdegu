from django.db import models


class Brewery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    established = models.DateField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Breweries'

    def __str__(self) -> str:
        return f"Browar {self.name}"
