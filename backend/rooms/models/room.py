from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Room(models.Model):
    class State(models.TextChoices):
        WAITING = 'WAITING', 'Waiting'
        STARTING = 'STARTING', 'Starting'
        IN_PROGRESS = 'IN_PROGRESS', 'In progress'
        FINISHED = 'FINISHED', 'Finished'

    name = models.CharField(
        unique=True, max_length=8,
        help_text='Unique room name'
    )
    password = models.CharField(
        max_length=20, null=True, blank=True,
        help_text='Password needed to join the room. Leave blank if you want the room to be public.'
    )
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rooms_hosted',
        on_delete=models.SET_NULL,
        null=True,
    )
    slots = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        help_text='Maximum number of participants in the room (including host)'
    )
    state = models.CharField(
        max_length=11,
        choices=State.choices,
        default=State.WAITING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserInRoom',
        related_name='rooms_joined',
        blank=True,
        help_text='Users currently present in the room'
    )
    beers = models.ManyToManyField(
        'beers.Beer',
        through='rooms.BeerInRoom',
        related_name='rooms',
        blank=True,
        help_text='Beers to be reviewed in the room'
    )

    def __str__(self):
        return f"'{self.name}' {self.users_count}/{self.slots} - {self.state.lower()}"

    @property
    def has_password(self) -> bool:
        return bool(self.password)

    @property
    def users_count(self) -> int:
        return self.users.count()
