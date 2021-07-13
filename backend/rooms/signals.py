from django.db.models.signals import post_save
from django.dispatch import receiver

from rooms.models import Room


@receiver(post_save, sender=Room)
def add_host_to_participants_on_create(sender, instance, created, **kwargs):
    """When Room is created, add its host to the list of participants."""
    if created and instance.host:
        instance.users.add(instance.host)

