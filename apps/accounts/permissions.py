from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator that checks if the user has one of the allowed roles.
    If not, shows an error message and redirects to the dashboard.
    ** Temporary bypass for admin@example.com **
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # TEMPORARY: allow the admin account to always pass (to break redirect loop)
            if request.user.is_authenticated and request.user.email == 'admin@example.com':
                return view_func(request, *args, **kwargs)

            if request.user.role not in allowed_roles:
                messages.error(request, "You don't have access to that page.")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator