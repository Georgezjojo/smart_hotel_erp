from django import forms
from .models import Reservation

class CheckinForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest', 'room', 'check_in', 'check_out', 'adults', 'children']