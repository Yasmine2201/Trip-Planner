from rest_framework import serializers

from budget.models import Expense, ExpenseGroup, ExpenseCategory

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
