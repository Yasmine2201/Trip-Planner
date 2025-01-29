from django.db import models

from core.models import User, Image
from trips.models import Trip


# Location
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()


class LocationPicture(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('location', 'picture')


class LocationPrice(models.Model):
    price_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True, default='')
    created_on = models.DateTimeField(null=True, auto_now=True)


# Visit
class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class VisitParticipation(models.Model):
    visit_participation_id = models.AutoField(primary_key=True)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class VisitParticipationStatus(models.TextChoices):
        ACCEPTED = 'accepted'
        PENDING = 'pending'
        DECLINED = 'declined'
    status = models.CharField(choices=VisitParticipationStatus, default=VisitParticipationStatus.PENDING)

    class Meta:
        unique_together = ('visit', 'user')


