from rest_framework.response import Response

from authentication.utils import ProtectableAPIView
from budget.models import Expense
from budget.serializers import ExpenseSerializer, CategorySerializer
from budget.services import BudgetService, ExpenseService, CategoryService
from trips.models import TripParticipation


class BudgetView(ProtectableAPIView):

    @staticmethod
    def __handle_budget(request, trip_id):
        user_id = request.user.user_id

        try:
            declared_budget = request.data['budget']
            declared_budget = BudgetService.declare_budget(user_id, trip_id, declared_budget)
            return Response(declared_budget, status=200)

        except TripParticipation.DoesNotExist:
            return Response({"error": f"TripParticipation not found"}, status=404)

    @staticmethod
    def post(request, trip_id):
        """
        Declare a budget for a trip.
        """
        return BudgetView.__handle_budget(request, trip_id)

    @staticmethod
    def put(request, trip_id):
        """
        Update a budget for a trip.
        """
        return BudgetView.__handle_budget(request, trip_id)

    @staticmethod
    def get(request, trip_id):
        """
        Get a budget for a trip.
        """

        user_id = request.user.user_id

        try:
            budget = BudgetService.get_budget(user_id, trip_id)
            return Response(budget, status=200)

        except TripParticipation.DoesNotExist:
            return Response({"error": f"TripParticipation not found"}, status=404)


############################################################################################################
class ExpenseView(ProtectableAPIView):

    @staticmethod
    def post(request, trip_id):
        """
        Declare an expense for a trip.
        """
        user_id = request.user.user_id
        expense_data = request.data
        try:
            expense = ExpenseService.declare_expense(user_id, trip_id, expense_data)
            expense_serializer = ExpenseSerializer(expense)
            return Response(expense_serializer.data, status=200)

        except TripParticipation.DoesNotExist:
            return Response({"error": f"TripParticipation deduced from the payload not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def put(request, trip_id, expense_id):
        """
        Update an expense for a trip.
        """
        user_id = request.user.user_id
        try:
            expense = ExpenseService.update_expense(user_id, trip_id, expense_id, request.data)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data, status=200)

        except Expense.DoesNotExist:
            return Response({"error": f"Expense {expense_id} not found"}, status=404)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def __get_all(request, trip_id):
        expenses = ExpenseService.get_all_expenses(request.user.user_id, trip_id)
        if expenses is None:
            return Response({"error": f"Expenses not found"}, status=404)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=200)

    @staticmethod
    def __get_by_id(request, trip_id, expense_id):
        try:
            expense = ExpenseService.get_expense_by_id(request.user.user_id, trip_id, expense_id)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data, status=200)

        except Expense.DoesNotExist:
            return Response({"error": f"Expense {expense_id} not found"}, status=404)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def get(request, trip_id, expense_id=None):
        """
            Get a specific expense for a trip or all expenses for a trip if no expense id is provided.
            """

        if expense_id is None:
            return ExpenseView.__get_all(request, trip_id)
        else:
            return ExpenseView.__get_by_id(request, trip_id, expense_id)

    @staticmethod
    def delete(request, trip_id, expense_id):
        """
        Delete an expense for a trip.
        """
        user_id = request.user.user_id
        try:
            expense = ExpenseService.delete_expense(user_id, trip_id, expense_id)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data, status=200)

        except Expense.DoesNotExist:
            return Response({"error": f"Expense {expense_id} not found"}, status=404)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)


############################################################################################################
class CategoryView(ProtectableAPIView):

    @staticmethod
    def get(request):
        """
        Get all categories.
        """
        categories = CategoryService.get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=200)
