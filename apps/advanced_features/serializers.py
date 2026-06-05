from rest_framework import serializers
from .models import DigitalKey

class DigitalKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalKey
        fields = '__all__'