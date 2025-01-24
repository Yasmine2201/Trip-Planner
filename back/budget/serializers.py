from rest_framework import serializers

from budget.models import Expense, ExpenseShare, ExpenseCategory
from visits.serializers import VisitSerializer


class ExpenseInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'name', 'description', 'planned_amount', 'actual_amount', 'is_shared', 'visit']
        extra_kwargs = {
            'visit': {'required': False},
            'planned_amount': {'required': False},
        }


class ExpenseSerializer(serializers.ModelSerializer):
    visit = VisitSerializer()
    class Meta:
        model = Expense
        fields = ['expense_id', 'category', 'name', 'description', 'planned_amount', 'actual_amount', 'is_shared', 'visit']


class DebtInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseShare
        fields = ['expense', 'with_user', 'due_amount', 'status']
        extra_kwargs = {
            'status': {'required': False}
        }


class RefundInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseShare
        fields = ['expense', 'with_user', 'refund_amount', 'status']
        extra_kwargs = {
            'status': {'required': False}
        }


class ExpenseShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseShare
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
