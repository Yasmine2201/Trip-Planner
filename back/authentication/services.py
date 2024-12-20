from datetime import datetime, timezone
from typing import Optional

from core.models import User
from core.services import UserService
from utils.auth_client import AuthSession, AuthClient


class AuthService:

    @staticmethod
    def login(email: str, password: str) -> tuple[AuthSession, User]:
        """
        Log in the user with the given email and password.
        :param email: The email of the user.
        :param password: The password of the user.
        :return: An AuthSession object.

        :raises InvalidCredentialsException: If the credentials are invalid.
        """
        auth_response = AuthClient().login(email, password)
        user = UserService.fetch_user(auth_response.user.id)
        return auth_response, user

    @staticmethod
    def register(email: str, password: str, alias: str, first_name: str, last_name: str, birthdate: Optional[str] = None) -> User:
        """
        Register the user with the given email and password.
        :param email: The email of the user.
        :param password: The password of the user.
        :param alias: The alias of the user.
        :param first_name: The first name of the user.
        :param last_name: The last name of the user.
        :param birthdate: The birthdate of the user.
        :return: An AuthSession object.

        :raises UserAlreadyExistsException: If the user already exists.
        :raises WeakPasswordException: If the password is weak.
        :raises InvalidRegisterRequestException: If the request is invalid
        """
        auth_response: AuthSession = AuthClient().register(email, password)
        user = User(
            user_id=auth_response.user.id,
            email=email,
            alias=alias,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate
        )
        user.save()
        return user

    @staticmethod
    def logout(token: str) -> None:
        """
        Log out the user with the given token.
        :param token: The token of the user.

        :raises BadTokenException: If the token is invalid.
        :raises SessionNotFound: If the session is not found.
        """
        AuthClient().logout(token)
