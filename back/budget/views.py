from django.core.serializers import serialize
from rest_framework.response import Response

from authentication.utils import TokenAuthentication, ProtectableAPIView
from budget.models import Expense, ExpenseGroup, ExpenseShare
from budget.serializers import ExpenseGroupInputSerializer, ExpenseGroupSerializer, ExpenseSerializer, \
    DebtInputSerializer, RefundInputSerializer, ExpenseShareSerializer
from budget.services import BudgetService, ExpenseGroupService, ExpenseService, ExpenseShareService
from trips.models import TripParticipation


class BudgetView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

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

class ExpenseGroupView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request,trip_id):
        """
        Declare an expense group for a trip.
        """
        user_id = request.user.user_id
        expense_group_data = request.data
        try :
            expense_gr = ExpenseGroupService.declare_expense_group(user_id, trip_id, expense_group_data)
            expense_gr_serializer = ExpenseGroupInputSerializer(expense_gr)
            return Response(expense_gr_serializer.data, status=200)

        except ValueError as e:
            return Response({"error" : str(e)}, status=400)
        except TripParticipation.DoesNotExist:
            return Response({"error": f"TripParticipation not found"}, status=404)

    @staticmethod
    def __get_all(request, trip_id):

        expense_grps = ExpenseGroupService.get_all_expense_groups(request.user.user_id, trip_id)
        if expense_grps is None:
            return Response({"error": f"Expense groups not found"}, status=404)
        else :
            serializer = ExpenseGroupSerializer(expense_grps, many=True)
            return Response(serializer.data, status=200)


    @staticmethod
    def __get_by_id(request, trip_id, expense_group_id):
        try :
            expense_gr = ExpenseGroupService.get_expense_group_by_id(request.user.user_id, trip_id, expense_group_id)
            serializer = ExpenseGroupSerializer(expense_gr)
            return Response(serializer.data, status=200)
        except ExpenseGroup.DoesNotExist:
            return Response({"error": f"Expense group {expense_group_id} not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def get(request, trip_id, expense_group_id = None):
            """
            Get a specific expense group for a trip or all expense groups for a trip if no expense group id is provided.
            """

            if expense_group_id is None:
                return ExpenseGroupView.__get_all(request, trip_id)
            else:
                return ExpenseGroupView.__get_by_id(request, trip_id, expense_group_id)
    @staticmethod
    def delete(request, trip_id, expense_group_id):
        """
        Delete an expense group for a trip.
        """
        user_id = request.user.user_id
        try :
            expense_gr = ExpenseGroupService.delete_expense_group(user_id, trip_id, expense_group_id)
            serializer = ExpenseGroupSerializer(expense_gr)
            return Response(serializer.data, status=200)

        except ExpenseGroup.DoesNotExist:
            return Response({"error": f"Expense group {expense_group_id} not found"}, status=404)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
############################################################################################################
class ExpenseView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request, trip_id):
        """
        Declare an expense for a trip.
        """
        user_id = request.user.user_id
        expense_data = request.data
        try :
            expense = ExpenseService.declare_expense(user_id, trip_id, expense_data)
            expense_serializer = ExpenseSerializer(expense)
            return Response(expense_serializer.data, status=200)

        except TripParticipation.DoesNotExist:
            return Response({"error": f"TripParticipation deduced from the payload not found"}, status=404)

        except Warning as w:
            return Response({"warning": str(w)}, status=400)


    @staticmethod
    def put(request, trip_id, expense_id):
        """
        Update an expense for a trip.
        """
        user_id = request.user.user_id
        try :
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
        try :
            expense = ExpenseService.get_expense_by_id(request.user.user_id, trip_id, expense_id)
            serializer = ExpenseSerializer(expense)
            return Response(serializer.data, status=200)

        except Expense.DoesNotExist:
            return Response({"error": f"Expense {expense_id} not found"}, status=404)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)


    @staticmethod
    def get(request, trip_id, expense_id = None):
            """
            Get a specific expense for a trip or all expenses for a trip if no expense id is provided.
            """

            if expense_id is None:
                return ExpenseView.__get_all(request, trip_id)
            else:
                return ExpenseView.__get_by_id(request, trip_id, expense_id)

############################################################################################################
class ExpenseShareView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def post(request, trip_id):
        """
        Declare a dept for an expense.
        """
        user_id = request.user.user_id
        shared_expense_data = request.data
        if 'due_amount' in shared_expense_data:
            serializer = DebtInputSerializer
        else:
            serializer = RefundInputSerializer

        try :
            shared_expense = ExpenseShareService.declare_debt(user_id, trip_id, shared_expense_data) \
                if serializer == DebtInputSerializer \
                else ExpenseShareService.declare_refund(user_id, trip_id, shared_expense_data)
            shared_expense_serializer = serializer(shared_expense)
            return Response(shared_expense_serializer.data, status=200)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

    @staticmethod
    def put(request, trip_id, share_id):
        """
        Update a dept for an expense.
        """
        user_id = request.user.user_id
        shared_expense_data = request.data
        if 'due_amount' in shared_expense_data:
            serializer = DebtInputSerializer
        else:
            serializer = RefundInputSerializer

        try :
            shared_expense = ExpenseShareService.update_debt(user_id, trip_id, share_id, shared_expense_data) \
                if serializer == DebtInputSerializer \
                else ExpenseShareService.update_refund(user_id, trip_id, share_id, shared_expense_data)
            shared_expense_serializer = serializer(shared_expense)
            return Response(shared_expense_serializer.data, status=200)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        except ExpenseShare.DoesNotExist:
            return Response({"error": f"Expense share {share_id} not found"}, status=404)

    @staticmethod
    def get(request, trip_id, share_id = None):
        """
        Get a specific dept for an expense or all depts for an expense if no dept id is provided.
        """
        if share_id :
            try :
                shared_expense = ExpenseShareService.get_expense_share_by_id(request.user.user_id, trip_id, share_id)
                return Response(ExpenseShareSerializer(shared_expense).data, status=200)

            except ExpenseShare.DoesNotExist:
                return Response({"error": f"Expense share {share_id} not found"}, status=404)

            except ValueError as e:
                return Response({"error": str(e)}, status=400)
        else :
            if 'debts' in request.path:
                shared_expenses = ExpenseShareService.get_all_debts(request.user.user_id, trip_id)
            elif 'refunds' in request.path:
                shared_expenses = ExpenseShareService.get_all_refunds(request.user.user_id, trip_id)
            else:
                shared_expenses = None

            if not shared_expenses:
                return Response({"error": f"Expense shares not found"}, status=404)

            else :
                return Response(ExpenseShareSerializer(shared_expenses, many=True).data, status=200)
    @staticmethod
    def delete(request, trip_id, share_id):
        """
        Delete a dept for an expense.
        """
        user_id = request.user.user_id
        try :
            shared_expense = ExpenseShareService.delete_expense_share(user_id, trip_id, share_id)
            shared_expense_serializer = ExpenseShareSerializer(shared_expense)
            return Response(shared_expense_serializer.data, status=200)

        except ExpenseShare.DoesNotExist:
            return Response({"error": f"Expense share {share_id} not found"}, status=404)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)

