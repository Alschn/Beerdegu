from rooms.models import Room


def check_if_room_exists(room_name: str) -> bool:
    return Room.objects.filter(name=room_name).exists()
