from core.models import User
from trips.models import Trip
from trips.services import TripService
from utils import ForbiddenActionError
from visits.models import Visit, Location, VisitParticipation
from visits.serializers import VisitSerializerInput


class VisitService:

    @staticmethod
    def create_visit(user: User, trip_id: int, visit_data: dict):
        """
        Create a new visit for a user in a trip.
        """

        visit_serializer = VisitSerializerInput(data=visit_data)
        visit_serializer.is_valid(raise_exception=True)

        visit_data_object = visit_serializer.validated_data
        trip: Trip = visit_data_object.get('trip')

        if trip.trip_id != trip_id:
            raise ValueError(f"Mismatch between trip_id in URL and trip_id in request body")

        if not TripService.check_participation(trip, user, is_owner=True):
            raise ForbiddenActionError(f"User is not part of the trip")

        visit = Visit.objects.create(**visit_data_object)

        trip_participations = TripService.get_trip_participations(trip.trip_id)

        for trip_participation in trip_participations:
            if trip_participation.user.user_id != user.user_id:
                VisitParticipation.objects.create(visit=visit, user=trip_participation.user)
            else:
                VisitParticipation.objects.create(visit=visit, user=user, status=VisitParticipation.VisitParticipationStatus.ACCEPTED)

        return visit

    @staticmethod
    def get_all_visits(user: User, trip_id: int):
        """
        Get all visits for a trip.
        """
        trip = TripService.get_user_trip_by_id(user, trip_id)

        return Visit.objects.filter(trip=trip)


class LocationService:
    # @staticmethod
    # def create_location(location_data: dict):
    #     location = Location.objects.create(**location_data)
    #     location.save()
    #     return location

    @staticmethod
    def get_all_locations():
        return Location.objects.all()
