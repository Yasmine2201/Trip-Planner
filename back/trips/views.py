from rest_framework import status
from rest_framework.response import Response

from authentication.utils import ProtectableAPIView, TokenAuthentication

from .models import Trip
from .serializers import TripSerializer
from .services import TripService


class TripView(ProtectableAPIView):

    authentication_classes = [TokenAuthentication]

    def get(self, request, trip_id=None):
        """
        Fetch all trips or a specific trip associated with a user.
        If a trip_id is provided, it fetches that specific trip.
        Otherwise, it fetches all trips for the user.
        """
        if trip_id is None:
            trips = TripService.get_all_user_trips(request.user)
            if not trips.exists():
                return Response({"error": "No trips available"}, status=404)
            serializer = TripSerializer(trips, many=True)
            return Response(serializer.data)
        else:
            try:
                trip = TripService.get_user_trip_by_id(trip_id)
                serializer = TripSerializer(trip)
                return Response(serializer.data)
            except Trip.DoesNotExist:
                return Response({"error": "Trip not found"}, status=404)
    @staticmethod
    def post(request):
        """
        Create a new trip and trip participation for a user.
        """
        if not request.data:
            return Response({"error": "Missing request body"}, status=status.HTTP_400_BAD_REQUEST)

        trip_payload = request.data
        try :
            trip = TripService.create_user_trip(trip_payload, request.user)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LastTripView(ProtectableAPIView):

    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request):
        """
        Fetch the last trip associated with a user.
        """
        try:
            trip = TripService.get_last_user_trip(request.user)
            serializer = TripSerializer(trip)
            return Response(serializer.data)
        except Trip.DoesNotExist:
            return Response({"error": "No trips available"}, status=404)
