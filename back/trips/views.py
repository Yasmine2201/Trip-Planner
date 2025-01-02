from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from back.authentication.utils import ProtectableAPIView, TokenAuthentication
from back.utils import NOT_FOUND_ERROR, ForbiddenActionError, INVALID_BODY_ERROR

from .models import Trip
from .serializers import TripSerializer
from .services import TripService


class TripView(ProtectableAPIView):

    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request: Request, trip_id: int = None):
        """
        Fetch all trips or a specific trip associated with a user.
        If a trip_id is provided, it fetches that specific trip.
        Otherwise, it fetches all trips for the user.
        """
        if trip_id is None:
            return TripView._get_all_trips(request)
        else:
            return TripView._get_trip_by_id(request, trip_id)

    @staticmethod
    def _get_trip_by_id(request: Request, trip_id: int) -> Response:
        try:
            trip = TripService.get_user_trip_by_id(request.user, trip_id)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=200)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def _get_all_trips(request: Request) -> Response:
        trips = TripService.get_all_user_trips(request.user)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=200)

    @staticmethod
    def post(request):
        """
        Create a new trip and trip participation for a user.
        """
        try:
            trip = TripService.create_user_trip(request.user, request.data)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": INVALID_BODY_ERROR, "detail": e.detail}, status=400)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def put(request, trip_id):
        """
        Update a specific trip associated with a user.
        """
        try:
            trip = TripService.update_user_trip(request.user, request.data, trip_id)
            serializer = TripSerializer(trip)
            return Response(serializer.data, status=200)
        except ValidationError as e:
            return Response({"error": INVALID_BODY_ERROR, "detail": e.detail}, status=400)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)

    @staticmethod
    def delete(request: Request, trip_id: int):
        """
        Delete a specific trip associated with a user.
        """
        try:
            TripService.delete_user_trip(request.user, trip_id)
            return Response(status=204)
        except Trip.DoesNotExist:
            return Response({"error": NOT_FOUND_ERROR.format(Model="Trip")}, status=404)
        except ForbiddenActionError as e:
            return Response({"error": e.msg}, status=403)


class LastTripView(ProtectableAPIView):

    @staticmethod
    def get(request):
        """
        Fetch the last trip associated with a user.
        """
        trip = TripService.get_last_user_trip(request.user)
        serializer = TripSerializer(trip)
        return Response(serializer.data)
