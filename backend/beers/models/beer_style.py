from django.db import models


class BeerStyle(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
