from budget.models import ExpenseGroup, Expense, ExpenseShare, ExpenseCategory
from budget.serializers import ExpenseInputSerializer, ExpenseGroupInputSerializer, RefundInputSerializer, \
    DebtInputSerializer
from trips.models import TripParticipation


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

class ExpenseGroupService:
    @staticmethod
    def declare_expense_group(user_id: str, trip_id: str, expense_group_data: dict):
        """
        Create a new expense group for a user in a trip and visit.
        """
        # Validate the data
        expense_group_serializer = ExpenseGroupInputSerializer(data=expense_group_data)
        expense_group_serializer.is_valid(raise_exception=True)
        # Deserialize the data
        expense_group_object = expense_group_serializer.validated_data

        # Check if the visit belongs to the trip
        visit = expense_group_object.get('visit')
        if visit.trip.trip_id != trip_id:
            raise ValueError(f"Visit {visit} belongs to trip {visit.trip} and not to trip {trip_id}")

        # Retrieve the trip participation associated with the user and trip
        trip_participation = TripParticipation.objects.get(user=user_id, is_owner=True, trip=trip_id)

        expense_group = ExpenseGroup.objects.create(trip_participation=trip_participation, **expense_group_object)
        return expense_group

    @staticmethod
    def get_all_expense_groups(user_id: str, trip_id: str):
        """
        Get all expense groups for a user in a trip.

        """
        return ExpenseGroup.objects.filter(trip_participation__user=user_id, trip_participation__trip=trip_id)

    @staticmethod
    def get_expense_group_by_id(user_id: str, trip_id: str, expense_group_id: str):
        """
        Get a specific expense group for a user in a trip.
        """
        expense_gr = ExpenseGroup.objects.get(expense_group_id=expense_group_id)
        if expense_gr.trip_participation.user.user_id != user_id or expense_gr.trip_participation.trip.trip_id != trip_id:
            raise ValueError(
                f"Mismatch between the url arguments and the attributes of the expense group {expense_group_id}")
        return expense_gr

    @staticmethod
    def delete_expense_group(user_id: str, trip_id: str, expense_group_id: str):
        """
        Delete an expense group for a user in a trip.
        """
        expense_group = ExpenseGroup.objects.get(expense_group_id=expense_group_id)
        if expense_group.trip_participation.user.user_id != user_id or expense_group.trip_participation.trip.trip_id != trip_id:
            raise ValueError(
                f"Mismatch between the url arguments and the attributes of the expense group {expense_group_id}")

        expenses = Expense.objects.filter(expense_group=expense_group)
        for expense in expenses:
            expense.expense_group = None
            expense.save()

        expense_group.delete()
        return expense_group


############################################################################################################

class ExpenseService:
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

        expense = Expense.objects.create(trip_participation=trip_participation, **expense_data_object)
        expense.save()

        if expense.is_shared:
            raise Warning("The expense is shared, please declare the debts or refunds")

        return expense

    @staticmethod
    def update_expense(user_id: str, trip_id: str, expense_id: str, expense_data: dict):
        """
        Update an expense for a user.
        """

        expense = Expense.objects.get(expense_id=expense_id)

        if expense.trip_participation.user.user_id != user_id or expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(f"Expense {expense_id} does not belong to user {user_id} in trip {trip_id}")

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


############################################################################################################
class ExpenseShareService:

    @staticmethod
    def get_potentials_creditors_debtors(user_id: str, trip_id: str):
        """
        Get the potential creditors and debtors for a user in a trip.
        """
        others_participants = TripParticipation.objects.filter(trip=trip_id).exclude(user=user_id)
        return others_participants

    @staticmethod
    def __declare_expense_share(user_id: str, trip_id: str, data: dict, serializer_class):
        """
        Create a new expense share (debt or refund) for a user.
        """
        # Validate the data
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        # Deserialize the data
        data_object = serializer.validated_data

        # Check if the expense in the payload belongs to the user and trip in the URL
        expense_id = data_object.get('expense').expense_id
        expense = Expense.objects.get(expense_id=expense_id)

        if expense.trip_participation.user.user_id != user_id or expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(
                f"Mismatch between the user or trip present in the URL arguments and the attributes of the expense {expense_id}"
                f" in the payload")

        if data_object.get("status") is None:
            data_object["status"] = "Created"

        expense_share = ExpenseShare.objects.create(**data_object)
        return expense_share

    @staticmethod
    def declare_debt(user_id: str, trip_id: str, debt_data: dict):
        return ExpenseShareService.__declare_expense_share(user_id, trip_id, debt_data, DebtInputSerializer)

    @staticmethod
    def declare_refund(user_id: str, trip_id: str, refund_data: dict):
        return ExpenseShareService.__declare_expense_share(user_id, trip_id, refund_data, RefundInputSerializer)

    @staticmethod
    def update_expense_share(user_id: str, trip_id: str, share_id: str, share_data: dict, serializer_class):
        """
        Update a debt or refund for a user.
        """
        share = ExpenseShare.objects.get(expense_share_id=share_id)
        if share.expense.trip_participation.user.user_id != user_id or share.expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(
                f"Mismatch between the user or trip present in the url arguments and the attributes of the expense"
                f" in the payload")

        share_serializer = serializer_class(data=share_data)
        share_serializer.is_valid(raise_exception=True)

        return share_serializer.update(share, share_serializer.validated_data)

    @staticmethod
    def update_debt(user_id: str, trip_id: str, debt_id: str, debt_data: dict):
        return ExpenseShareService.update_expense_share(user_id, trip_id, debt_id, debt_data, DebtInputSerializer)

    @staticmethod
    def update_refund(user_id: str, trip_id: str, refund_id: str, refund_data: dict):
        return ExpenseShareService.update_expense_share(user_id, trip_id, refund_id, refund_data, RefundInputSerializer)

    @staticmethod
    def get_all_debts(user_id: str, trip_id: str):
        """
        Get all debts for a user in a trip.
        """
        return ExpenseShare.objects.filter(expense__trip_participation__user=user_id,
                                           expense__trip_participation__trip=trip_id, refund_amount=None)

    @staticmethod
    def get_all_refunds(user_id: str, trip_id: str):
        """
        Get all refunds for a user in a trip.
        """
        return ExpenseShare.objects.filter(expense__trip_participation__user=user_id,
                                           expense__trip_participation__trip=trip_id, due_amount=None)

    @staticmethod
    def get_expense_share_by_id(user_id: str, trip_id: str, expense_share_id: str):
        """
        Get a specific debt or refund for a user in a trip.
        """
        expense_share = ExpenseShare.objects.get(expense_share_id=expense_share_id)
        if expense_share.expense.trip_participation.user.user_id != user_id or expense_share.expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(
                f"Mismatch between the user or trip present in the url arguments and the attributes of the expense"
                f" in the refund payload")
        return expense_share

    @staticmethod
    def delete_expense_share(user_id: str, trip_id: str, expense_share_id: str):
        """
        Delete a debt or refund for a user in a trip.
        """
        expense_share = ExpenseShare.objects.get(expense_share_id=expense_share_id)
        if expense_share.expense.trip_participation.user.user_id != user_id or expense_share.expense.trip_participation.trip.trip_id != trip_id:
            raise ValueError(
                f"Mismatch between the user or trip present in the url arguments and the attributes of the expense"
                f" in the refund payload")
        expense_share.delete()
        return expense_share


############################################################################################################
class CategoryService:
    # @staticmethod
    # def create_category(name: str):
    #     category = ExpenseCategory.objects.create(name=name)
    #     category.save()
    #     return category

    @staticmethod
    def get_category(category_id: str):
        category = ExpenseCategory.objects.get(category_id=category_id)
        return category

    @staticmethod
    def get_all_categories():
        return ExpenseCategory.objects.all()

    # @staticmethod
    # def update_category(category_id: str, name: str):
    #     category = ExpenseCategory.objects.get(category_id=category_id)
    #     category.name = name
    #     category.save()
    #     return category
    #
    # @staticmethod
    # def delete_category(category_id: str):
    #     category = ExpenseCategory.objects.get(category_id=category_id)
    #     category.delete()
    #     return category
