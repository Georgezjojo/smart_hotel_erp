from apps.hotel.models import Room

def available_rooms(request):
    return {'available_rooms': Room.objects.filter(status='available')}