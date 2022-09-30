from django.db import models


class Hop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=1000, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
