from rest_framework import status
from rest_framework.response import Response

from authentication.utils import ProtectableAPIView, TokenAuthentication

from .models import Trip, TripParticipation
from .serializers import TripSerializer


class TripView(ProtectableAPIView):

    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):

        user_id = request.user.user_id

        trip_participations = TripParticipation.objects.filter(user_id=user_id)

        trip_ids = [trip.trip_id.id for trip in trip_participations]
        trips = Trip.objects.filter(id__in=trip_ids)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

