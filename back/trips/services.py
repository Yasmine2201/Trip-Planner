from core.models import User
from trips.models import TripParticipation, Trip


class TripService:
    @staticmethod
    def get_all_user_trips(user : User):
        """
        Fetch all trips associated with a user.
        """
        user_trip_participations = TripParticipation.objects.filter(user=user.user_id)
        user_trip_ids = [trip.trip_id for trip in user_trip_participations]
        return Trip.objects.filter(trip_id__in=user_trip_ids)

    @staticmethod
    def get_user_trip_by_id(trip_id: int):
        """
        Fetch a specific trip associated with a user.
        """
        return Trip.objects.get(trip_id=trip_id)

    @staticmethod
    def get_last_user_trip(user:User):
        """
        Fetch the last trip associated with a user.
        """
        user_trip_participations = TripParticipation.objects.filter(user=user.user_id)
        user_trip_ids = [trip.trip_id for trip in user_trip_participations]
        return Trip.objects.filter(trip_id__in=user_trip_ids).latest('start_date')

    @staticmethod
    def create_user_trip(trip_payload : dict, user: User):
        """
        Create a new trip and trip participation for a user (return the trip object).
        The required fields are: trip_name, start_date, end_date, latitude, longitude, radius.
        Image is optional

        """
        required_fields = ['trip_name', 'start_date', 'end_date', 'latitude', 'longitude', 'radius']
        if not all(field in trip_payload for field in required_fields):
            raise ValueError(f"Missing required fields to create a trip: {', '.join([field for field in required_fields if field not in trip_payload])}")
        else:
            trip = Trip.objects.create(trip_name=trip_payload['trip_name'],
                                       start_date=trip_payload['start_date'],
                                       end_date=trip_payload['end_date'],
                                       latitude=trip_payload['latitude'],
                                       longitude=trip_payload['longitude'],
                                       radius=trip_payload['radius'])
            if 'image' in trip_payload:
                trip.image = trip_payload['image']

            user = User.objects.get(user_id=user.user_id)
            participation_trip = TripParticipation.objects.create(trip=trip, user=user, is_owner=True)

            trip.save()
            participation_trip.save()

            return trip

    @staticmethod
    def update_user_trip(trip_id: int, trip_payload: dict):
        """
        Update a trip associated with a user.
        """
        trip = Trip.objects.get(trip_id=trip_id)
        for field, value in trip_payload.items():
            setattr(trip, field, value)
        trip.save()
        return trip

    @staticmethod
    def delete_user_trip(trip_id: int):
        """
        Delete a trip associated with a user.
        """
        trip = Trip.objects.get(trip_id=trip_id)
        trip.delete()


