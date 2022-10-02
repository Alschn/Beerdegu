from django_q.tasks import schedule, Schedule
from django.core.management import call_command


def flush_expired_tokens() -> str:
    return call_command('flushexpiredtokens')


def schedule_flush_expired_tokens() -> Schedule:
    return schedule(
        'django.core.management.call_command',
        'flushexpiredtokens',
        name='Remove expired tokens',
        schedule_type=Schedule.DAILY,
        repeats=-1,
    )
