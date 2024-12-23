from rest_framework import status
from rest_framework.response import Response

from authentication.utils import ProtectableAPIView
from .serializers import TripSerializer
from .service import TripService


class TripListView(ProtectableAPIView):

    @staticmethod
    def get(request):
        trips = TripService.get_user_trips(request.user)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
