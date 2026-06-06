from django.shortcuts import redirect

class RedirectAuthenticatedUsersMiddleware:
    """
    If a user is authenticated and tries to access any of the listed
    public-only pages, redirect them to the dashboard.
    (The homepage redirect is handled in the home view.)
    """
    PUBLIC_ONLY_PATHS = [
        '/accounts/login/',
        '/accounts/register/',
        '/accounts/password/reset/',
        '/accounts/password/change/',
        '/terms/',
        '/contact/',
        '/privacy/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path
            if any(path.startswith(p) for p in self.PUBLIC_ONLY_PATHS):
                return redirect('dashboard')
        return self.get_response(request)