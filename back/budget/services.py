from trips.models import TripParticipation


class BudgetService:

    @staticmethod
    def declare_budget(user_id : str, trip_id : str, declared_budget : float):
        trip_participation = TripParticipation.objects.get(user=user_id, trip=trip_id)

        trip_participation.declared_budget = declared_budget
        trip_participation.save()
        return trip_participation.declared_budget


    @staticmethod
    def get_budget(user_id : str, trip_id : str):
        trip_participation = TripParticipation.objects.get(user=user_id, trip=trip_id)
        return trip_participation.declared_budget