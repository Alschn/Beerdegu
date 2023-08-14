from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.text import slugify


def get_file_path(instance: 'Beer', filename: str) -> str:
    _, extension = filename.split('.')
    slug = slugify(instance.name)
    random_part = get_random_string(length=8)
    name = f"{slug}-{random_part}.{extension}"
    return f"beers/{name}"


class Beer(models.Model):
    name = models.CharField(max_length=60)
    brewery = models.ForeignKey(
        'beers.Brewery',
        related_name='beers',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    style = models.ForeignKey(
        'beers.BeerStyle',
        related_name='beers',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    percentage = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0'))]
    )
    volume_ml = models.PositiveIntegerField(
        help_text="Volume of the beer in milliliters [mL]"
    )
    hop_rate = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Grams of hops per liter [g/L]"
    )
    extract = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Concentration of dissolved solids (mainly sugars) in a brewery wort. [°BLG]"
    )
    IBU = models.PositiveIntegerField(
        null=True, blank=True,
        help_text="Bitterness measured in International Bitterness Units scale"
    )
    image = models.ImageField(
        null=True, blank=True,
        upload_to=get_file_path,
        max_length=255,
    )
    description = models.TextField(max_length=1000, null=True, blank=True)
    hops = models.ManyToManyField(
        'beers.Hop',
        related_name='beers',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        to_str = f"{self.name} {self.percentage}% {self.volume_ml}ml"
        if self.brewery:
            to_str += f", {self.brewery}"
        return to_str
