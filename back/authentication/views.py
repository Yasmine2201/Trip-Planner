from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import LoginInputSerializer, AuthErrorSerializer, UserSerializer, \
    RegisterInputSerializer
from authentication.utils import set_supabase_cookies, ACCESS_TOKEN_COOKIE_NAME, remove_supabase_cookies
from core.models import User
from utils.auth_client import AuthClient, AuthSession, AuthException, InvalidCredentialsException, BadTokenException, \
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

            email: str = request_serializer.validated_data['email']
            password: str = request_serializer.validated_data['password']

            auth_response: AuthSession = AuthClient().login(email, password)
            response_serializer = UserSerializer(auth_response)

            response = Response(response_serializer.data, status=200)
            set_supabase_cookies(response, auth_response)
            return response

        except InvalidCredentialsException as e:
            return handle_auth_error(e, 401)


class LogoutView(APIView):

    @staticmethod
    def post(request: Request):
        try:
            access_token: str = request.COOKIES.get(ACCESS_TOKEN_COOKIE_NAME)
            if not access_token:
                return handle_auth_error(AuthException("validation_failed", "invalid"), 400)

            AuthClient().logout(access_token)
            response = Response(status=204)
            remove_supabase_cookies(response)
            return response

        except BadTokenException as e:
            return handle_auth_error(e, 403)

        except SessionNotFound as e:
            return handle_auth_error(e, 409)


class RegisterView(APIView):

    @staticmethod
    def post(request: Request):
        try:
            request_serializer = RegisterInputSerializer(data=request.data)
            if not request_serializer.is_valid():
                return handle_auth_error(AuthException.from_validation_error(request_serializer.errors), 400)

            email: str = request_serializer.validated_data['email']
            password: str = request_serializer.validated_data['password']

            auth_response: AuthSession = AuthClient().register(email, password)

            user: User = User(
                userId=auth_response.user.id,
                email=email,
                alias=request_serializer.validated_data['alias'],
                first_name=request_serializer.validated_data['first_name'],
                last_name=request_serializer.validated_data['last_name'],
                birthdate=request_serializer.validated_data.get('birthdate')
            )
            user.save()

            response = Response(status=201)
            return response

        except (UserAlreadyExistsException, WeakPasswordException, InvalidRegisterRequestException) as e:
            return handle_auth_error(e, 400)
