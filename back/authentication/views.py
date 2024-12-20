from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import LoginInputSerializer, AuthErrorSerializer, RegisterInputSerializer
from authentication.services import AuthService
from authentication.utils import set_supabase_cookies, ACCESS_TOKEN_COOKIE_NAME, remove_supabase_cookies, \
    TokenAuthentication, CustomAPIView
from core.serializers import UserSerializer
from utils.auth_client import AuthException, InvalidCredentialsException, BadTokenException, \
    SessionNotFound, UserAlreadyExistsException, WeakPasswordException, InvalidRegisterRequestException


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

            session, user = AuthService.login(**request_serializer.validated_data)
            response_serializer = UserSerializer(user)

            response = Response(response_serializer.data, status=200)
            set_supabase_cookies(response, session)
            return response

        except InvalidCredentialsException as e:
            return handle_auth_error(e, 401)

        except AuthException as e:
            return handle_auth_error(e, 400)


class LogoutView(CustomAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request: Request):
        response = Response(status=500)
        try:
            access_token: str = request.COOKIES.get(ACCESS_TOKEN_COOKIE_NAME)
            if not access_token:
                return handle_auth_error(AuthException("validation_failed", "invalid"), 400)
            AuthService.logout(access_token)

            if hasattr(request, 'auth') and hasattr(request.auth, 'auth_session'):
                request.auth = None

            response = Response(status=204)

        except BadTokenException as e:
            response = handle_auth_error(e, 403)

        except SessionNotFound as e:
            response = handle_auth_error(e, 409)

        finally:
            remove_supabase_cookies(response)
            return response


class RegisterView(APIView):

    @staticmethod
    def post(request: Request):
        try:
            request_serializer = RegisterInputSerializer(data=request.data)
            if not request_serializer.is_valid():
                return handle_auth_error(AuthException.from_validation_error(request_serializer.errors), 400)

            AuthService.register(**request_serializer.validated_data)

            response = Response(status=201)
            return response

        except (UserAlreadyExistsException, WeakPasswordException, InvalidRegisterRequestException) as e:
            return handle_auth_error(e, 400)
