from django.shortcuts import render
from rest_framework.response import Response

from authentication.utils import TokenAuthentication, ProtectableAPIView
from budget.services import BudgetService
from trips.serializers import TripParticipationSerializer


# Create your views here.
class BudgetView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def handle_budget(request, trip_id):
        user_id = request.user.user_id

        try:
            declared_budget = request.data['budget']
            declared_budget = BudgetService.declare_budget(user_id, trip_id, declared_budget)
            return Response(declared_budget, status=200)

        except Exception as e:
            return Response({"error": f"An error occurred while processing the budget, Here are the details: '{e}'"}, status=400)

    @staticmethod
    def post(request, trip_id):
        """
        Declare a budget for a trip.
        """
        return BudgetView.handle_budget(request, trip_id)

    @staticmethod
    def put(request, trip_id):
        """
        Update a budget for a trip.
        """
        return BudgetView.handle_budget(request, trip_id)

    @staticmethod
    def get(request, trip_id):
            """
            Get a budget for a trip.
            """

            user_id = request.user.user_id

            try:
                budget = BudgetService.get_budget(user_id, trip_id)
                return Response(budget, status=200)

            except Exception as e:
                return Response({"error": f"An error occurred while fetching the budget: {e}"}, status=400)