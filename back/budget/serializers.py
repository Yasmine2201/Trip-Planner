from rest_framework import serializers

from budget.models import Expense, ExpenseCategory
from visits.models import Visit
from visits.serializers import VisitSerializer


class ExpenseInputSerializer(serializers.ModelSerializer):
    visit_id = serializers.IntegerField(required=False)

    class Meta:
        model = Expense
        fields = ['category', 'name', 'description', 'planned_amount', 'actual_amount', 'visit_id']

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
        fields = ['expense_id', 'category', 'name', 'description', 'planned_amount', 'actual_amount', 'visit']

    visit = PartialVisitSerializer()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
