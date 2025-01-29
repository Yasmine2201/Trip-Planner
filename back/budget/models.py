from django.db import models
from rest_framework.exceptions import ValidationError

from core.models import User
from trips.models import TripParticipation
from visits.models import Visit


def validate_category(value):
    if value not in map(lambda x: x[0], ExpenseCategory.CATEGORY_CHOICES):
        raise ValidationError(f'{value} is not a valid category')


# Create your models here.
class ExpenseCategory(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Accommodation', 'Accommodation'),
        ('Activity', 'Activity'),
        ('Shopping', 'Shopping'),
        ('Visit', 'Visit'),
        ('Others', 'Others'),
    ]
    name = models.CharField(max_length=255, primary_key=True, choices=CATEGORY_CHOICES, default='Others',
                            validators=[validate_category])

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures all validators, including choices, are applied
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Category {self.name}'


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    trip_participation = models.ForeignKey(TripParticipation, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    planned_amount = models.FloatField(null=True, blank=True)
    actual_amount = models.FloatField(null=True, blank=True)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f' Expense{self.name} - {self.planned_amount} - {self.actual_amount}'
