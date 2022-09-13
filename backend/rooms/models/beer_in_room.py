from django.db import models


class BeerInRoom(models.Model):
    """ManyToMany Through Rooms and Beers."""

    beer = models.ForeignKey('beers.Beer', on_delete=models.CASCADE)
    room = models.ForeignKey('rooms.Room', on_delete=models.CASCADE)
    ratings = models.ManyToManyField('rooms.Rating', related_name='belongs_to', blank=True)

    class Meta:
        verbose_name_plural = 'Beers in Room'

    def __str__(self) -> str:
        return f"{self.room.name} - {self.beer}"
