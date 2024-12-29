from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from trips.models import TripParticipation
from .models import Notification
from .serializers import NotificationSerializer
from .utils import publish_notification


@receiver(post_save, sender=TripParticipation)
def create_notification(sender, instance, created, **kwargs):
    print(f"Creating notification for Trip Participation: {instance.trip_participation_id}")
    if created:
        notification = Notification.objects.create(
            user = instance.user,
            type="Type XXX",
            content=f"Trip Participation {instance.trip_participation_id} has been created",
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()
        publish_notification(instance.user.user_id, NotificationSerializer(notification).data)
    print(f"Notification created for Trip Participation: {instance.trip_participation_id}")
