from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import TokenAuthentication
from core.serializers import UserSerializer


# Create your views here.
class CurrentUserView(APIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, 200)
