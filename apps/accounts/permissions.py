from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps


def role_required(allowed_roles):
    """
    Decorator that checks if the user is authenticated and has one of the allowed roles.
    Redirects to login if not authenticated, raises PermissionDenied otherwise.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator