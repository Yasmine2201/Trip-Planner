from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import LoginInputSerializer, AuthErrorSerializer, UserSerializer
from authentication.utils import set_supabase_cookies, ACCESS_TOKEN_COOKIE_NAME, REFRESH_TOKEN_COOKIE_NAME
from utils.auth_client import AuthClient, AuthSession, AuthException, InvalidCredentialsException, BadTokenException, \
    SessionNotFound


def handle_auth_error(e: AuthException, status_code: int) -> Response:
    error_serializer = AuthErrorSerializer(e)
    return Response(error_serializer.data, status=status_code)


class LoginView(APIView):

    @staticmethod
    def post(request: Request):
        try:
            request_serializer = LoginInputSerializer(data=request.data)
            if not request_serializer.is_valid():
                return handle_auth_error(AuthException.from_validation_error(request_serializer.errors), 400)

            email: str = request_serializer.validated_data['email']
            password: str = request_serializer.validated_data['password']

            auth_response: AuthSession = AuthClient().login(email, password)
            response_serializer = UserSerializer(auth_response)

            response = Response(response_serializer.data, status=200)
            set_supabase_cookies(response, auth_response)
            return response

        except InvalidCredentialsException as e:
            return handle_auth_error(e, 401)

        except AuthException as e:
            return handle_auth_error(e, 400)

    def get(self, request: Request):
        print(request.COOKIES)
        return Response(status=204)


class LogoutView(APIView):

    @staticmethod
    def post(request: Request):
        try:
            access_token: str = request.COOKIES.get(ACCESS_TOKEN_COOKIE_NAME)
            if not access_token:
                return handle_auth_error(AuthException("validation_failed", "invalid"), 400)

            AuthClient().logout(access_token)
            response = Response(status=204)
            response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
            response.delete_cookie(REFRESH_TOKEN_COOKIE_NAME)
            return response

        except BadTokenException as e:
            return handle_auth_error(e, 403)

        except SessionNotFound as e:
            return handle_auth_error(e, 409)
