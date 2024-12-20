from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.utils import TokenAuthentication, CustomAPIView
from core.serializers import UserSerializer


# Create your views here.
class CurrentUserView(CustomAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, 200)
