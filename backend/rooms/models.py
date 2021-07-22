from typing import Optional

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from beers.models import Beer


class Room(models.Model):
    ROOM_STATE_CHOICES = [
        ('WAITING', 'WAITING'),
        ('STARTING', 'STARTING'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('FINISHED', 'FINISHED'),
    ]

    name = models.CharField(unique=True, max_length=8)
    password = models.CharField(max_length=20, null=True, blank=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='host')
    slots = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    state = models.CharField(max_length=11, choices=ROOM_STATE_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='UserInRoom', blank=True)
    beers = models.ManyToManyField(Beer, through='BeerInRoom', blank=True)

    def __str__(self):
        return f"'{self.name}' {self.users.all().count()}/{self.slots} - {self.state.lower()}"


class Rating(models.Model):
    color = models.TextField(max_length=300, blank=True, null=True)
    foam = models.TextField(max_length=300, blank=True, null=True)
    smell = models.TextField(max_length=300, blank=True, null=True)
    taste = models.TextField(max_length=300, blank=True, null=True)
    opinion = models.TextField(max_length=300, blank=True, null=True)
    note = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ], null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['id']

    # noinspection PyUnresolvedReferences
    def __str__(self) -> str:
        to_str = f"{self.note} by {self.added_by}"
        rating_for: Optional[BeerInRoom] = self.belongs_to.all().first()
        if rating_for:
            return f"{rating_for} - {to_str}"
        return to_str


class BeerInRoom(models.Model):
    """ManyToMany Through Rooms and Beers."""
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    ratings = models.ManyToManyField('Rating', related_name='belongs_to', blank=True)

    class Meta:
        verbose_name_plural = 'Beers in Room'

    def __str__(self) -> str:
        return f"{self.room.name} - {self.beer}"


class UserInRoom(models.Model):
    """ManyToMany Through Rooms and Users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Users in Room'

    def __str__(self) -> str:
        return f"{self.user.username} - {self.room.name}"
