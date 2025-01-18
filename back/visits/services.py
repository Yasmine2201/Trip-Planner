from trips.models import TripParticipation
from visits.models import Visit
from visits.serializers import VisitSerializerInput


class VisitService:

    @staticmethod
    def create_visit(user_id: str, trip_id: str, visit_data: dict):
        """
        Create a new visit for a user in a trip.
        """

        visit_serializer = VisitSerializerInput(data=visit_data)
        visit_serializer.is_valid(raise_exception=True)

        visit_data_object = visit_serializer.validated_data

        if visit_data_object.get('trip').trip_id != trip_id:
            raise ValueError(f"Mismatch between trip_id in URL and trip_id in request body")
        if not TripParticipation.objects.filter(user=user_id, trip=trip_id).exists():
            raise ValueError(f"User {user_id} is not participating in the trip {trip_id}")

        visit = Visit.objects.create(**visit_data_object)

        return visit

    @staticmethod
    def get_all_visits(trip_id: str):
        """
        Get all visits for a trip.
        """

        return Visit.objects.filter(trip=trip_id)
