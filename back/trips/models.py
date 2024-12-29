from django.db import models

from core.models import User, Image


class Trip(models.Model):

    trip_id = models.AutoField(primary_key=True)
    trip_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField()
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Trip(id={self.trip_id}, name={self.trip_name}, start_date={self.start_date}, end_date={self.end_date}, latitude={self.latitude}, longitude={self.longitude})"


class TripParticipation(models.Model):

    trip_participation_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField()
    declared_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"TripParticipation(id={self.trip_participation_id}, trip_id={self.trip_id}, user_id={self.user_id})"
