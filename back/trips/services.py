from rest_framework.exceptions import ValidationError

from core.models import User
from trips.models import TripParticipation, Trip
from trips.serializers import TripSerializer, TripInputSerializer
from utils import ForbiddenActionError


class TripService:
    @staticmethod
    def get_all_user_trips(user: User) -> list[Trip]:
        """
        Fetch all trips associated with a user.
        """
        user_trip_participations = TripParticipation.objects.filter(user=user.user_id)
        user_trip_ids = [trip.trip_id for trip in user_trip_participations]
        return Trip.objects.filter(trip_id__in=user_trip_ids)

    @staticmethod
    def get_user_trip_by_id(from_user: User, trip_id: int) -> Trip:
        """
        Fetch a specific trip associated with a user.
        """
        trip: Trip = Trip.objects.get(trip_id=trip_id)
        if not TripService._is_trip_from_user(trip, from_user):
            raise ForbiddenActionError("Trip does not belong to user")
        return trip

    @staticmethod
    def get_last_user_trip(user: User):
        """
        Fetch the last trip associated with a user (latest start date).
        """
        user_trip_participations = TripParticipation.objects.filter(user=user.user_id)
        user_trip_ids = [trip.trip_id for trip in user_trip_participations]
        return Trip.objects.filter(trip_id__in=user_trip_ids).latest('start_date')

    @staticmethod
    def create_user_trip(from_user: User, trip_data: dict) -> Trip:
        """
        Create a new trip and trip participation for a user (return the trip object).
        The required fields are: trip_name, start_date, end_date, latitude, longitude, radius.
        """
        trip_serializer = TripInputSerializer(data=trip_data)
        trip_serializer.is_valid(raise_exception=True)
        trip = trip_serializer.create(trip_serializer.validated_data)

        trip_participation = TripParticipation.objects.create(trip=trip, user=from_user, is_owner=True)
        trip_participation.save()

        return trip

    @staticmethod
    def update_user_trip(from_user: User, trip_data: dict, trip_id: int) -> Trip:
        """
        Update a trip associated with a user.
        """
        if trip_data is None or 'trip_id' not in trip_data or trip_data['trip_id'] != trip_id:
            raise ValidationError("Body should contain a trip id which matches the URL")

        trip = Trip.objects.get(trip_id=trip_id)
        trip_serializer = TripInputSerializer(trip, data=trip_data)
        trip_serializer.is_valid(raise_exception=True)

        if not TripService._is_trip_from_user(trip, from_user, is_owner=True):
            raise ForbiddenActionError("User is not the owner of the trip.")

        updated_trip = trip_serializer.update(trip, trip_serializer.validated_data)
        return updated_trip

    @staticmethod
    def delete_user_trip(from_user: User, trip_id: int) -> Trip:
        """
        Delete a trip associated with a user.
        """
        trip = Trip.objects.get(trip_id=trip_id)

        if not TripService._is_trip_from_user(trip, from_user, is_owner=True):
            raise ForbiddenActionError("User is not the owner of the trip.")

        trip.delete()
        return trip

    @staticmethod
    def _is_trip_from_user(trip: Trip, user: User, is_owner: bool = False) -> bool:
        """
        Check if a trip belongs to a user.

        :param trip: Trip object
        :param user: User object
        :param is_owner: Check if the user is the owner of the trip

        :return: True if the trip belongs to the user, False otherwise
        """
        if is_owner:
            return TripParticipation.objects.filter(trip=trip, user=user, is_owner=True).exists()
        return TripParticipation.objects.filter(trip=trip, user=user).exists()
