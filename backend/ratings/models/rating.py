from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Rating(models.Model):
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='ratings',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    beer = models.ForeignKey(
        'beers.Beer',
        related_name='ratings',
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        'rooms.Room',
        related_name='ratings',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    color = models.TextField(max_length=300, blank=True, null=True)
    foam = models.TextField(max_length=300, blank=True, null=True)
    smell = models.TextField(max_length=300, blank=True, null=True)
    taste = models.TextField(max_length=300, blank=True, null=True)
    opinion = models.TextField(max_length=300, blank=True, null=True)
    note = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self) -> str:
        to_str = f'{self.beer.name} - {self.note or "?"} by {self.added_by}'
        if self.room is not None:
            to_str += f' in room {self.room.name}'
        return to_str
