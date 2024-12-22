import os

import jwt
from dotenv import load_dotenv
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from core.models import User
from utils.auth_client import AuthSession, AuthClient, InvalidRefreshToken

load_dotenv()
SUPABASE_SIGNING_KEY = os.getenv("SUPABASE_SIGNING_KEY")

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


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request: Request) -> tuple[User, dict]:
        access_token = request.COOKIES.get(ACCESS_TOKEN_COOKIE_NAME)
        refresh_token = request.COOKIES.get(REFRESH_TOKEN_COOKIE_NAME)

        if not access_token and not refresh_token:
            raise AuthenticationFailed("Authentication credentials were not provided")

        auth = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        try:
            payload = jwt.decode(access_token, SUPABASE_SIGNING_KEY, algorithms=["HS256"], audience="authenticated")

        except jwt.ExpiredSignatureError:
            try:
                auth_session = AuthClient().refresh_token(refresh_token)
                payload = jwt.decode(auth_session.access_token, SUPABASE_SIGNING_KEY, algorithms=["HS256"],
                                     audience="authenticated")
                auth = {
                    'access_token': auth_session.access_token,
                    'refresh_token': auth_session.refresh_token,
                    'new_session': auth_session
                }
            except InvalidRefreshToken:
                raise AuthenticationFailed("Token has expired and refresh token is invalid")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        try:
            user = User.objects.get(user_id=payload['sub'])
            return user, auth
        except User.DoesNotExist:
            raise AuthenticationFailed("User not found")


def _replace_token_in_response(request: Request, response: Response) -> Response:
    if hasattr(request, 'auth') and request.auth is not None and 'new_session' in request.auth:
        set_supabase_cookies(response, request.auth['new_session'])
    return response


class ProtectableAPIView(APIView):

    authentication_classes = [TokenAuthentication]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        return _replace_token_in_response(request, response)


class ProtectableGenericAPIView(GenericAPIView):

    authentication_classes = [TokenAuthentication]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        return _replace_token_in_response(request, response)


class ProtectableCreateAPIView(CreateModelMixin, ProtectableAPIView):
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProtectableListAPIView(ListModelMixin, ProtectableAPIView):
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProtectableRetrieveAPIView(RetrieveModelMixin, ProtectableAPIView):
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ProtectableDestroyAPIView(DestroyModelMixin, ProtectableAPIView):
    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProtectableUpdateAPIView(UpdateModelMixin, ProtectableAPIView):
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ProtectableListCreateAPIView(ListModelMixin, CreateModelMixin, ProtectableAPIView):
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProtectableRetrieveUpdateAPIView(RetrieveModelMixin, UpdateModelMixin, ProtectableAPIView):
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProtectableRetrieveDestroyAPIView(RetrieveModelMixin, DestroyModelMixin, ProtectableAPIView):
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProtectableRetrieveUpdateDestroyAPIView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin,
                                              ProtectableAPIView):
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProtectableViewSet(ViewSetMixin, ProtectableAPIView):
    pass


class ProtectableGenericViewSet(ViewSetMixin, ProtectableGenericAPIView):
    pass


class ProtectableReadOnlyModelViewSet(RetrieveModelMixin, ListModelMixin, ProtectableGenericViewSet):
    pass


class ProtectableModelViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin,
                              ProtectableGenericViewSet):
    pass
