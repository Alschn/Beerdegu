from django.contrib.postgres.fields import DecimalRangeField, IntegerRangeField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class BeerStyle(models.Model):
    name = models.CharField(max_length=60)
    known_as = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text=_("Other names for this beer style (comma separated)")
    )
    country = CountryField(blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    serving_temperature_range = DecimalRangeField(
        blank=True, null=True,
        help_text=_("Temperature measured in Celsius")
    )
    abv_range = DecimalRangeField(
        blank=True, null=True,
        help_text=_("Alcohol by volume measured in percentages")
    )
    color_range = IntegerRangeField(
        blank=True, null=True,
        help_text=_("Color described in EBC (European Brewery Convention) units")
    )
    bitterness_range = IntegerRangeField(
        blank=True, null=True,
        help_text=_("Bitterness described in IBU (International Bitterness Units)")
    )
    original_gravity_range = DecimalRangeField(
        blank=True, null=True,
        help_text=_("Original gravity measured in degrees Plato")
    )
    final_gravity_range = DecimalRangeField(
        blank=True, null=True,
        help_text=_("Final gravity measured in degrees Plato")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # todo: color hex range field

    class Meta:
        verbose_name = _("Beer Style")
        verbose_name_plural = _("Beer Styles")

    def __str__(self) -> str:
        return self.name
