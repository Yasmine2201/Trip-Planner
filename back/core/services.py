from pydantic import ValidationError

from core.models import User
from core.serializers import UserInputSerializer
from utils import ForbiddenActionError


class UserService:

    @staticmethod
    def fetch_user(user_id: str) -> User:
        return User.objects.get(user_id=user_id)

    @staticmethod
    def update_user(from_user: User, user_data: dict) -> User:
        """
        Update user
        """
        if user_data is None or 'user_id' not in user_data:
            raise ValidationError("Body shoumd contain a user id")

        user = User.objects.get(user_id=user_data['user_id'])
        user_serializer = UserInputSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)

        if from_user.user_id != user_data['user_id']:
            raise ForbiddenActionError("A user can only update its own data")

        updated_user = user_serializer.update(user, user_serializer.validated_data)
        return updated_user

    @staticmethod
    def fetch_all_users():
        """
        Fetch all users present in the database.
        """
        return User.objects.all()

    @staticmethod
    def fetch_user_by_id(user_id: str):
        """
        Fetch a specific user by user_id.
        """
        return User.objects.get(user_id=user_id)
