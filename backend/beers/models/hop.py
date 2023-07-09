from django.db import models


class Hop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"
