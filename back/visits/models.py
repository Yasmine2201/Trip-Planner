from django.db import models

from core.models import User, Image
from trips.models import Trip


# Create your models here.
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()


class Visit(models.Model):
    visit_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class LocationPicture(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    picture = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('location', 'picture')


class VisitParticipation(models.Model):
    class VisitParticipationStatus(models.TextChoices):
        ACCEPTED = 'accepted'
        PENDING = 'pending'
        DECLINED = 'declined'

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=VisitParticipationStatus, default=VisitParticipationStatus.PENDING)

    class Meta:
        unique_together = ('visit', 'user')
