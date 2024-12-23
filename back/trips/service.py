from core.models import User
from trips.models import Trip, TripParticipation


class TripService:

    @staticmethod
    def get_user_trips(user: User) -> list[Trip]:
        """
        Get all trips that a user is participating in.
        :param user: User instance
        :return: List of Trip instances that the user is participating in
        """
        trip_participations = TripParticipation.objects.filter(user_id=user.user_id)
        trip_ids = [trip.trip.trip_id for trip in trip_participations]
        return Trip.objects.filter(trip_id__in=trip_ids)
