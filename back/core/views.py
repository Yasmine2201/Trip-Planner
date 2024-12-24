from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import TokenAuthentication, ProtectableAPIView
from core.models import User
from core.serializers import UserSerializer
from core.services import UserService


# Create your views here.
class CurrentUserView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, 200)

    @staticmethod
    def put(request):
        if not request.data:
            return Response({"error": "Missing request body"}, 400)
        else :
            try :
                user_payload = request.data
                user = UserService.update_user(request.user.user_id, user_payload)
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, status=200)

            except User.DoesNotExist:
                return Response({"error": "User not found"}, 404)

class OtherUsersView(APIView):
    @staticmethod
    def get(request, user_id=None):
        """
        Fetch all users or a specific user by user_id.
        """
        if user_id is not None:
            try:
                user = UserService.fetch_user_by_id(user_id)
                user_serializer = UserSerializer(user)
                return Response(user_serializer.data, 200)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, 404)

        else:
            try:
                users = UserService.fetch_all_users()
                user_serializer = UserSerializer(users, many=True)
                return Response(user_serializer.data, 200)
            except User.DoesNotExist:
                return Response({"error": "No users available"}, 404)


