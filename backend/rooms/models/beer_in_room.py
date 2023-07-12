from django.db import models
from ordered_model.models import OrderedModel


class BeerInRoom(OrderedModel):
    """ManyToMany Through Rooms and Beers."""

    beer = models.ForeignKey(
        'beers.Beer',
        related_name='rooms_through',
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        'rooms.Room',
        related_name='beers_through',
        on_delete=models.CASCADE
    )
    ratings = models.ManyToManyField(
        'rooms.Rating',
        related_name='belongs_to',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_with_respect_to = ('room',)

    class Meta(OrderedModel.Meta):
        verbose_name_plural = 'Beers in Room'

    def __str__(self) -> str:
        return f"{self.room.name} - #{self.order} - {self.beer}"
