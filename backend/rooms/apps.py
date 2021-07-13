from django.apps import AppConfig


class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'

    def ready(self) -> None:
        from . import signals
