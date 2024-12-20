from core.models import User


class UserService:

    @staticmethod
    def fetch_user(user_id: str) -> User:
        return User.objects.get(user_id=user_id)
