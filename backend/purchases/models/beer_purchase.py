import datetime
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class BeerPurchase(models.Model):
    # todo: add nullable foreign key to location (?) model

    class Packaging(models.TextChoices):
        BOTTLE = 'BOTTLE', _('Bottle')
        CAN = 'CAN', _('Can')
        KEG = 'KEG', _('Keg')
        DRAUGHT = 'DRAUGHT', _('Draught')

    beer = models.ForeignKey(
        'beers.Beer',
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    sold_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='beer_purchases'
    )
    packaging = models.CharField(
        max_length=7,
        choices=Packaging.choices
    )
    price = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text=_('Price of the beer in Polish Zloty [PLN]'),
        validators=[MinValueValidator(Decimal('0'))]
    )
    volume_ml = models.PositiveIntegerField(
        help_text=_('Volume of the beer in milliliters [mL]')
    )
    image = models.ImageField(
        upload_to='purchases/',
        help_text=_('Image of the receipt, menu or the beer itself'),
        blank=True, null=True
    )
    purchased_at = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Beer Purchase')
        verbose_name_plural = _('Beer Purchases')
