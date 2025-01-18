from django.db import models
from rest_framework.exceptions import ValidationError

from core.models import User
from trips.models import TripParticipation
from visits.models import Visit


def validate_category(value):
    valid_categories = ['Food', 'Transport', 'Accommodation', 'Activity', 'Others']
    if value not in valid_categories:
        raise ValidationError(f'{value} is not a valid category')

# Create your models here.
class ExpenseCategory(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Accommodation', 'Accommodation'),
        ('Activity', 'Activity'),
        ('Others', 'Others'),
    ]
    name = models.CharField(max_length=255, primary_key=True, choices=CATEGORY_CHOICES, default='Others', validators=[validate_category])

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures all validators, including choices, are applied
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Category {self.name}'

class ExpenseGroup(models.Model):
    expense_group_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey(Visit,on_delete=models.CASCADE, null=True)
    trip_participation = models.ForeignKey(TripParticipation,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f'Expense Group {self.name} - {self.visit} - {self.trip_participation}'


class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    trip_participation = models.ForeignKey(TripParticipation,on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    planned_amount = models.FloatField(null=True, blank=True)
    actual_amount = models.FloatField(null=True, blank=True)
    is_shared = models.BooleanField(default=False)
    expense_group = models.ForeignKey(ExpenseGroup,on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f' Expense{self.name} - {self.planned_amount} - {self.actual_amount}'


class ExpenseShare(models.Model):
    expense_share_id = models.AutoField(primary_key=True)
    expense = models.ForeignKey(Expense,on_delete=models.CASCADE)
    with_user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    due_amount = models.FloatField(null=True, blank=True)
    refund_amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f'ExpenseShare {self.expense} - {self.with_user} - {self.due_amount} - {self.refund_amount} - {self.status}'