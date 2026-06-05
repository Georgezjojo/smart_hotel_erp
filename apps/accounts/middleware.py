from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Exclude certain paths from the redirect (password change itself, logout, and static/media)
            exempt_paths = [
                reverse('password_change'),
                reverse('logout'),
                '/accounts/password/change/',   # fallback just in case
            ]
            current_path = request.path_info

            if request.user.must_change_password and current_path not in exempt_paths:
                # Allow AJAX requests to go through (so toast notifications still work)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    pass
                else:
                    return redirect('password_change')

        response = self.get_response(request)
        return response