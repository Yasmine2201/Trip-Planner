from __future__ import annotations

from typing import Optional

from attr import dataclass
from dotenv import load_dotenv
import httpx
import os

from utils import Singleton, make_jwt_header

__ALL__ = ["AuthClient",
           "AuthSession",
           "AuthUser",
           "AuthException",
           "InvalidCredentialsException",
           "UserAlreadyExistsException",
           "WeakPasswordException",
           "InvalidRegisterRequestException",
           "BadTokenException",
           "SessionNotFound",
           "InvalidRefreshToken",
           ]

load_dotenv()
URL: str = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_KEY")


class AuthClient(metaclass=Singleton):
    """
    AuthClient is a class that allows you to interact with the Supabase Auth API to perform actions such as login,
    registration, logout, and token refresh. It is a Singleton class, so it is recommended to use the get() method to
    get the instance of the class.

    Contrary to the SupabaseClient, the AuthClient is not bound to a session and is perftectly stateless.
    """

    def __init__(self, url: str = URL, key: str = SUPABASE_SERVICE_KEY):
        self.__http_client: httpx.Client = httpx.Client(
            base_url=f"{url}/auth/v1",
            headers={
                "apikey": key,
                "Content-Type": "application/json;charset=UTF-8"
            }
        )

    def login(self, email: str, password: str) -> AuthSession:
        """
        Login the user using the email and password provided.
        :param email: The email of the user
        :param password: The password of the user
        :return: An AuthSession object

        :raises InvalidCredentialsException: If the credentials are invalid
        """
        credentials = {
            "email": email,
            "password": password
        }
        response: httpx.Response = self.__http_client.post(
            "/token",
            params="grant_type=password",
            json=credentials
        )
        content: dict = response.json()

        if response.status_code != 200:
            self._raise_auth_exception(content)

        return self._parse_auth_response(content)

    def register(self, email: str, password: str) -> AuthSession:
        """
        Register the user using the email and password provided.
        :param email: The email of the user
        :param password: The password of the user
        :return: An AuthSession object

        :raises UserAlreadyExistsException: If the user already exists
        :raises WeakPasswordException: If the password is weak
        :raises InvalidRegisterRequestException: If the request is invalid
        """
        credentials = {
            "email": email,
            "password": password
        }
        response: httpx.Response = self.__http_client.post(
            "/signup",
            json=credentials
        )
        content: dict = response.json()

        if response.status_code != 200:
            self._raise_auth_exception(content)

        return self._parse_auth_response(content)

    def logout(self, token: str) -> None:
        """
        Logout the user using the token provided.
        :param token: The token of the user

        :raises BadTokenException: If the token is invalid
        :raises SessionNotFound: If the session does not exist
        """
        response: httpx.Response = self.__http_client.post(
            "/logout",
            headers=make_jwt_header(token)
        )

        if response.status_code != 204:
            self._raise_auth_exception(response.json())

    def refresh_token(self, refresh_token: str) -> AuthSession:
        """
        Refresh the token using the refresh token provided.
        :param refresh_token: The refresh token
        :return: An AuthSession object

        :raises InvalidRefreshToken: If the refresh token is invalid
        """
        data = {
            "refresh_token": refresh_token
        }
        response: httpx.Response = self.__http_client.post(
            "/token",
            params="grant_type=refresh_token",
            json=data
        )
        content = response.json()

        if response.status_code != 200:
            self._raise_auth_exception(content)

        return self._parse_auth_response(content)

    def __del__(self):
        self.__http_client.close()

    @staticmethod
    def get() -> AuthClient:
        """
        Get the instance of the AuthClient or create a new one if it does not exist.
        """
        return AuthClient()

    @staticmethod
    def _parse_auth_response(response: dict) -> AuthSession:
        user: Optional[AuthUser] = None
        session: Optional[AuthSession] = None

        if "user" in response:
            user = AuthUser(
                id=response["user"]["id"],
                email=response["user"]["email"],
                role=response["user"]["role"]
            )

        return AuthSession(
            user=user,
            access_token=response["access_token"],
            refresh_token=response["refresh_token"],
            expires_in=response["expires_in"],
            expires_at=response["expires_at"],
            token_type=response["token_type"]
        )

    @staticmethod
    def _raise_auth_exception(response: dict):
        msg: str = response.get("msg")
        code: str = response.get("error_code")

        raise exceptions_code.get(code, AuthException(msg, code))


# TYPES
@dataclass
class AuthSession:
    user: Optional[AuthUser]
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: int
    token_type: str


@dataclass
class AuthUser:
    id: str
    email: str
    role: str


# EXCEPTIONS
class AuthException(Exception):
    def __init__(self, message: str = '', code: str = ''):
        super().__init__(message, code)
        self.message = message
        self.code = code


class InvalidCredentialsException(AuthException):
    code = 'invalid_credentials'

    def __init__(self, message: str = 'Invalid credentials'):
        super().__init__(message, self.code)


class UserAlreadyExistsException(AuthException):
    code = 'user_already_exists'

    def __init__(self, message: str = 'User already exists'):
        super().__init__(message, self.code)


class WeakPasswordException(AuthException):
    code = 'weak_password'

    def __init__(self, message: str = 'Weak password'):
        super().__init__(message, self.code)


class InvalidRegisterRequestException(AuthException):
    code = 'validation_failed'

    def __init__(self, message: str = 'Invalid request'):
        super().__init__(message, self.code)


class BadTokenException(AuthException):
    code = 'bad_jwt'

    def __init__(self, message: str = 'Bad token'):
        super().__init__(message, self.code)


class SessionNotFound(AuthException):
    code = 'session_not_found'

    def __init__(self, message: str = 'Session not found'):
        super().__init__(message, self.code)


class InvalidRefreshToken(AuthException):
    code = 'refresh_token_not_found'

    def __init__(self, message: str = 'Invalid refresh token'):
        super().__init__(message, self.code)


exceptions_code: dict = {
    exception.code: exception for exception in [
        InvalidCredentialsException,
        UserAlreadyExistsException,
        WeakPasswordException,
        InvalidRegisterRequestException,
        BadTokenException,
        SessionNotFound,
        InvalidRefreshToken
    ]
}
