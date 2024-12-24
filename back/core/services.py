from django.db.models import QuerySet

from core.models import User


class UserService:

    @staticmethod
    def fetch_user(user_id: str) -> User:
        return User.objects.get(user_id=user_id)

    @staticmethod
    def update_user(user_id: str, user_payload: dict) -> User:
        user = User.objects.get(user_id=user_id)
        for key, value in user_payload.items():
            setattr(user, key, value)
        user.save()
        return user

    @staticmethod
    def fetch_all_users():
        """
        Fetch all users present in the database.
        """
        return User.objects.all()

    @staticmethod
    def fetch_user_by_id(user_id: str) :
        """
        Fetch a specific user by user_id.
        """
        return User.objects.get(user_id=user_id)