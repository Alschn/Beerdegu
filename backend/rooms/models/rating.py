from typing import Optional

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from rooms.models import BeerInRoom


class Rating(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
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

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        to_str = f"{self.note} by {self.added_by}"
        rating_for: Optional[BeerInRoom] = self.belongs_to.all().first()
        if rating_for:
            return f"{rating_for} - {to_str}"
        return to_str
