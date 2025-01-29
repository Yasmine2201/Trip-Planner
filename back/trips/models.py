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
        return f"{self.trip_name} from {self.start_date} to {self.end_date}"


class TripParticipation(models.Model):
    trip_participation_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_owner = models.BooleanField()
    declared_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('trip', 'user')

    def __str__(self):
        return f"TripParticipation(id={self.trip_participation_id}, trip_id={self.trip_id}, user_id={self.user_id})"


class TripInvitation(models.Model):
    class TripInvitationStatus(models.TextChoices):
        ACCEPTED = 'accepted'
        PENDING = 'pending'
        DECLINED = 'declined'

    trip_invitation_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(choices=TripInvitationStatus, default=TripInvitationStatus.PENDING)

    class Meta:
        unique_together = ('trip', 'sender', 'receiver')
