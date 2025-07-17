from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


def year_validator(value: int):
    now = timezone.now()

    if value < 1000 or value > now.year:
        raise ValidationError(
            _("%(value)s is not an valid year."),
            params={"value": value},
        )


def get_brewery_image_path(instance: 'Brewery', filename: str) -> str:
    _, extension = filename.split('.')
    slug = slugify(instance.name)
    random_part = get_random_string(length=8)
    name = f"{slug}-{random_part}.{extension}"
    return f"breweries/{name}"


class Brewery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = CountryField(blank=True, null=True)
    year_established = models.PositiveIntegerField(
        null=True, blank=True,
        validators=[year_validator]
    )
    website = models.URLField(null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True,
        upload_to=get_brewery_image_path,
        max_length=255,
    )
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Brewery')
        verbose_name_plural = _('Breweries')

    def __str__(self) -> str:
        return self.name
