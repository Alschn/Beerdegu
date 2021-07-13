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
    host = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='host')
    slots = models.PositiveIntegerField(default=1, validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    state = models.CharField(max_length=11, choices=ROOM_STATE_CHOICES, default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through='UserInRoom', blank=True)
    beers = models.ManyToManyField(Beer, through='BeerInRoom', blank=True)


class Rating(models.Model):
    color = models.TextField(max_length=300, blank=True, null=True)
    foam = models.TextField(max_length=300, blank=True, null=True)
    smell = models.TextField(max_length=300, blank=True, null=True)
    taste = models.TextField(max_length=300, blank=True, null=True)
    opinion = models.TextField(max_length=300, blank=True, null=True)
    note = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(10),
    ])
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class BeerInRoom(models.Model):
    """ManyToMany Through Rooms and Beers."""
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    ratings = models.ManyToManyField('Rating')

    class Meta:
        verbose_name_plural = 'Beers in Room'


class UserInRoom(models.Model):
    """ManyToMany Through Rooms and Users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Users in Room'
