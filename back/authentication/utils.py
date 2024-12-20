from rest_framework.response import Response

from utils.auth_client import AuthSession


ACCESS_TOKEN_COOKIE_NAME = "sb-access-token"
REFRESH_TOKEN_COOKIE_NAME = "sb-refresh-token"


def set_supabase_cookies(response: Response, session: AuthSession):
    response.set_cookie(
        ACCESS_TOKEN_COOKIE_NAME,
        session.access_token,
        expires=session.expires_at,
        httponly=True,
        secure=True,
        samesite="None"
    )

    response.set_cookie(
        REFRESH_TOKEN_COOKIE_NAME,
        session.refresh_token,
        httponly=True,
        secure=True,
        samesite="None"
    )


def remove_supabase_cookies(response: Response):
    response.set_cookie(
        ACCESS_TOKEN_COOKIE_NAME,
        max_age=0,
        httponly=True,
        secure=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        samesite="None",
    )
    response.set_cookie(
        REFRESH_TOKEN_COOKIE_NAME,
        max_age=0,
        httponly=True,
        secure=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        samesite="None",
    )
