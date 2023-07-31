from datetime import timedelta

from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import schedule

from core.shared.queue import get_function_module_path
from rooms.models import UserInRoom

DEFAULT_INACTIVE_USERS_REMOVAL_MINUTES = 24 * 60


def remove_inactive_users_in_rooms(minutes: int = DEFAULT_INACTIVE_USERS_REMOVAL_MINUTES):
    """Remove inactive users from rooms."""

    now = timezone.now()
    users_in_rooms = UserInRoom.objects.filter(
        last_active__lte=now - timedelta(minutes=minutes)
    )
    return users_in_rooms.delete()


def schedule_inactive_users_in_rooms_removal(*args, **kwargs) -> Schedule:
    return schedule(
        get_function_module_path(remove_inactive_users_in_rooms),
        *args,
        name='Remove inactive users from rooms',
        schedule_type=Schedule.DAILY,
        repeats=-1,
        **kwargs
    )
