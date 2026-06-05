from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'profile_picture',
            'address', 'city', 'country', 'bio'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'phone': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'address': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'city': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'country': forms.TextInput(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition'}),
            'bio': forms.Textarea(attrs={'class': 'w-full border border-slate-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'text-sm'}),
        }