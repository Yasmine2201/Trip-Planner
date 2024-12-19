from rest_framework.response import Response

from utils.auth_client import AuthSession


ACCESS_TOKEN_COOKIE_NAME = "sb-access-token"
REFRESH_TOKEN_COOKIE_NAME = "sb-refresh-token"


def set_supabase_cookies(response: Response, session: AuthSession):
    response.set_cookie(
        ACCESS_TOKEN_COOKIE_NAME,
        session.access_token,
        max_age=session.expires_in,
        httponly=True,
        secure=True,
        samesite="Strict"
    )

    response.set_cookie(
        REFRESH_TOKEN_COOKIE_NAME,
        session.refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict"
    )
