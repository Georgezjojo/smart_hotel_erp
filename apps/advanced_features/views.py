from rest_framework import viewsets
from .models import DigitalKey
from .serializers import DigitalKeySerializer

class DigitalKeyViewSet(viewsets.ModelViewSet):
    queryset = DigitalKey.objects.all()
    serializer_class = DigitalKeySerializer