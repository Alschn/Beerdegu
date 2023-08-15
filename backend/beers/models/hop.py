from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Hop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Hop')
        verbose_name_plural = _('Hops')

    def __str__(self) -> str:
        return self.name
