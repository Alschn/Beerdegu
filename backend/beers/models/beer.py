from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Beer(models.Model):
    name = models.CharField(max_length=60)
    brewery = models.ForeignKey('beers.Brewery', on_delete=models.SET_NULL, null=True, blank=True)
    style = models.ForeignKey('beers.BeerStyle', on_delete=models.SET_NULL, null=True, blank=True)
    percentage = models.DecimalField(
        max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0'))]
    )
    volume_ml = models.PositiveIntegerField()
    hop_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Grams of hops per liter [g/L]")
    extract = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Concentration of dissolved solids (mainly sugars) in a brewery wort. [°BLG]"
    )
    IBU = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Bitterness measured in International Bitterness Units scale"
    )
    image = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    hops = models.ManyToManyField('beers.Hop', blank=True)

    def __str__(self) -> str:
        to_str = f"{self.name} {self.percentage}% {self.volume_ml}ml"
        if self.brewery:
            to_str += f", {self.brewery}"
        return to_str
