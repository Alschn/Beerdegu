from django.conf import settings

from django.db import models


class UserInRoom(models.Model):
    """ManyToMany Through Rooms and Users."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rooms_joined_through',
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        'rooms.Room',
        on_delete=models.CASCADE
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Users in Room'

    def __str__(self) -> str:
        return f"{self.user.username} - {self.room.name}"
