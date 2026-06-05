from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('staff/', views.staff_management, name='staff_management'),
    path('password/change/', views.password_change, name='password_change'),

    # Password reset (forgot password)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/forgot_password.html',
             email_template_name='accounts/password_reset_email.html',
             success_url='/accounts/password-reset/done/'
         ),
         name='forgot_password'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'  # you can reuse reset_password.html or create one
         ),
         name='password_reset_complete'),
]