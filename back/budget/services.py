from budget.models import Expense, ExpenseCategory
from budget.serializers import ExpenseInputSerializer
from trips.models import TripParticipation
from visits.models import Visit, VisitParticipation


class BudgetService:

    @staticmethod
    def declare_budget(user_id: str, trip_id: str, declared_budget: float):
        trip_participation = TripParticipation.objects.get(user=user_id, trip=trip_id)

        trip_participation.declared_budget = declared_budget
        trip_participation.save()
        return trip_participation.declared_budget

    @staticmethod
    def get_budget(user_id: str, trip_id: str):
        trip_participation = TripParticipation.objects.get(user=user_id, trip=trip_id)
        return trip_participation.declared_budget


############################################################################################################
class ExpenseService:

    @staticmethod
    def __check_visit_of_expense(user_id: str, trip_id: str, expense_data: dict):
        visit = expense_data.get('visit')
        if visit is not None:
            visit = Visit.objects.get(visit_id=visit.visit_id)
            print("visit", visit, type(visit))
            if visit.trip.trip_id != trip_id:
                raise ValueError(f"Visit {visit.name} does not belong to trip {trip_id}")

            if not VisitParticipation.objects.filter(visit=visit, user=user_id).exists():
                raise ValueError(f"User {user_id} is not a participant of visit {visit.name}")

    @staticmethod
    def declare_expense(user_id: str, trip_id: str, expense_data: dict):
        """
        Create a new expense for a user.
        """
        # Validate the data
        expense_serializer = ExpenseInputSerializer(data=expense_data)
        expense_serializer.is_valid(raise_exception=True)

        # Deserialize the data
        expense_data_object = expense_serializer.validated_data

        # Retrieve the trip participation associated with the user and trip
        trip_participation = TripParticipation.objects.get(user=user_id, is_owner=True, trip=trip_id)

        ExpenseService.__check_visit_of_expense(user_id, trip_id, expense_data_object)

        expense = Expense.objects.create(trip_participation=trip_participation, **expense_data_object)
        expense.save()

        return expense

    @staticmethod
    def update_expense(user_id: str, trip_id: str, expense_id: str, expense_data: dict):
        """
        Update an expense for a user.
        """

        expense = Expense.objects.get(expense_id=expense_id)
        if expense.trip_participation.user.user_id != user_id or expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(f"Expense {expense_id} does not belong to user {user_id} in trip {trip_id}")

        ExpenseService.__check_visit_of_expense(user_id, trip_id, expense_data)

        expense_serializer = ExpenseInputSerializer(data=expense_data)
        expense_serializer.is_valid(raise_exception=True)

        return expense_serializer.update(expense, expense_serializer.validated_data)

    @staticmethod
    def get_all_expenses(user_id: str, trip_id: str):
        """
        Get all expenses for a user in a trip.
        """
        return Expense.objects.filter(trip_participation__user=user_id, trip_participation__trip=trip_id)

    @staticmethod
    def get_expense_by_id(user_id: str, trip_id: str, expense_id: str):
        """
        Get a specific expense for a user in a trip.
        """
        expense = Expense.objects.get(expense_id=expense_id)
        if expense.trip_participation.user.user_id != user_id or expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(f"Expense {expense_id} does not belong to user {user_id} in trip {trip_id}")
        return expense

    @staticmethod
    def delete_expense(user_id: str, trip_id: str, expense_id: str):
        """
        Delete an expense for a user in a trip.
        """
        expense = Expense.objects.get(expense_id=expense_id)
        if expense.trip_participation.user.user_id != user_id or expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(f"Expense {expense_id} does not belong to user {user_id} in trip {trip_id}")
        expense.delete()
        return expense


############################################################################################################
class CategoryService:
    @staticmethod
    def get_category(category_id: str):
        category = ExpenseCategory.objects.get(category_id=category_id)
        return category

    @staticmethod
    def get_all_categories():
        return ExpenseCategory.objects.all()
