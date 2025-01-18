from rest_framework import serializers

from budget.models import Expense, ExpenseGroup, ExpenseShare


class ExpenseGroupInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseGroup
        fields = ['visit', 'name', 'description']


class ExpenseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseGroup
        fields = '__all__'


class ExpenseInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['category', 'name', 'description', 'planned_amount', 'actual_amount', 'is_shared', 'expense_group']
        extra_kwargs = {
            'expense_group': {'required': False}
        }


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


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
