from authentication.utils import set_supabase_cookies


class RefreshTokenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if hasattr(request, 'auth') and hasattr(request.auth, 'auth_session'):
            set_supabase_cookies(response, request.auth.auth_session)

        return response
