from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import User
from apps.notifications.models import Notification


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.must_change_password = True   # force password change on first login
            user.save()
            login(request, user)
            return redirect('dashboard')       # middleware will redirect to password change
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            # Create a welcome notification
            Notification.objects.create(
                recipient=user,
                message=f"Welcome back, {user.get_full_name() or user.email}!",
                channel='in_app'
            )
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def staff_management(request):
    if request.user.role not in ['super_admin', 'owner', 'manager']:
        messages.error(request, 'Access denied')
        return redirect('dashboard')
    staff = User.objects.exclude(role='guest')
    return render(request, 'accounts/staff_management.html', {'staff': staff})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            request.user.must_change_password = False
            request.user.save()
            messages.success(request, 'Your password has been changed successfully.')
            if request.user.role != 'guest':
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {
        'form': form,
        'forced': request.user.must_change_password,
    })