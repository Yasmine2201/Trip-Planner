from pydantic import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import LoginInputSerializer, AuthErrorSerializer, UserSerializer
from authentication.utils import set_supabase_cookies
from utils.auth_client import AuthClient, AuthSession, AuthException, InvalidCredentialsException


class LoginView(APIView):

    @staticmethod
    def post(request: Request):
        try:
            request_serializer = LoginInputSerializer(data=request.data)
            if not request_serializer.is_valid():
                error_serializer = AuthErrorSerializer({
                    "msg": request_serializer.errors,
                    "error_code": "invalid_request_data"
                })
                return Response(error_serializer.data, status=400)

            email: str = request_serializer.validated_data['email']
            password: str = request_serializer.validated_data['password']

            auth_response: AuthSession = AuthClient().login(email, password)
            response_serializer = UserSerializer(auth_response)

            response = Response(response_serializer.data, status=200)
            set_supabase_cookies(response, auth_response)
            return response

        except InvalidCredentialsException as e:
            error_serializer = AuthErrorSerializer(e)
            return Response(error_serializer.data, status=401)

        except AuthException as e:
            error_serializer = AuthErrorSerializer(e)
            return Response(error_serializer.data, status=400)
