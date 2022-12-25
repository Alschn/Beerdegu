from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Room(models.Model):
    class State(models.TextChoices):
        WAITING = 'WAITING', 'Waiting'
        STARTING = 'STARTING', 'Starting'
        IN_PROGRESS = 'IN_PROGRESS', 'In progress'
        FINISHED = 'FINISHED', 'Finished'

    name = models.CharField(unique=True, max_length=8)
    password = models.CharField(max_length=20, null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='host')
    slots = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    state = models.CharField(max_length=11, choices=State.choices, default=State.WAITING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='UserInRoom', blank=True)
    beers = models.ManyToManyField('beers.Beer', through='rooms.BeerInRoom', blank=True)

    def __str__(self):
        return f"'{self.name}' {self.users.all().count()}/{self.slots} - {self.state.lower()}"

    @property
    def has_password(self) -> bool:
        return bool(self.password)
