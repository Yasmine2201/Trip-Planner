from rest_framework import serializers

from budget.models import Expense, ExpenseShare, ExpenseCategory
from visits.models import Visit
from visits.serializers import VisitSerializer


class ExpenseInputSerializer(serializers.ModelSerializer):
    visit_id = serializers.IntegerField()

    class Meta:
        model = Expense
        fields = ['category', 'name', 'description', 'planned_amount', 'actual_amount', 'is_shared', 'visit_id']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        visit_id = instance['visit_id']
        if 'visit_id' in data:
            del data['visit_id']
        data['visit'] = Visit.objects.get(visit_id=visit_id)

        return data


class ExpenseSerializer(serializers.ModelSerializer):
    class PartialVisitSerializer(VisitSerializer):
        class Meta:
            model = Visit
            fields = ['visit_id', 'name']

    class Meta:
        model = Expense
        fields = ['expense_id', 'category', 'name', 'description', 'planned_amount', 'actual_amount', 'is_shared', 'visit']

    visit = PartialVisitSerializer()


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
