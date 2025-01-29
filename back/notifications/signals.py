import json
from dataclasses import dataclass

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from budget.models import Expense
from trips.models import TripParticipation, TripInvitation
from visits.models import VisitParticipation
from .models import Notification


@dataclass
class NotificationContent:
    message: str
    data: dict

    def __str__(self):
        return json.dumps(self.__dict__)


@receiver(post_save, sender=VisitParticipation)
def create_visit_participation_notification(sender, instance: VisitParticipation, created, **kwargs):
    if created and instance.status == VisitParticipation.VisitParticipationStatus.PENDING:
        content = NotificationContent(
            message="notifications.content.visit-request",
            data={
                "visitName": instance.visit.name,
                "tripName": instance.visit.trip.trip_name,
                "tripId": instance.visit.trip.trip_id,
                "startDate": instance.visit.start_date,
                "endDate": instance.visit.end_date
            }
        )

        notification = Notification.objects.create(
            user=instance.user,
            type="VisitRequest",
            content=str(content),
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()


@receiver(post_save, sender=TripParticipation)
def create_trip_participation_notification(sender, instance, created, **kwargs):
    print(f"Creating notification for Trip Participation: {instance.trip_participation_id}")
    print(kwargs)
    if created:
        content = NotificationContent(
            message="notifications.content.added-to-trip",
            data={
                "tripName": instance.trip.trip_name,
                "tripId": instance.trip.trip_id
            }
        )

        notification = Notification.objects.create(
            user=instance.user,
            type="AddToTrip",
            content=str(content),
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()
    print(f"Notification created for Trip Participation: {instance.trip_participation_id}")


@receiver(post_save, sender=TripParticipation)
def notify_budget_initialization(sender, instance, created, **kwargs):
    if not created and instance.declared_budget != 0:
        content = NotificationContent(
            message="notifications.content.budget-changed",
            data={
                "tripName": instance.trip.trip_name,
                "budget": instance.declared_budget,
                "tripId": instance.trip.trip_id
            }
        )

        notification = Notification.objects.create(
            user=instance.user,
            type="Budget",
            content=str(content),
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()
    print(
        f"Notified user {instance.user.user_id} about budget initialization for Trip Participation: {instance.trip_participation_id}")


@receiver(post_save, sender=Expense)
def notify_expenses_exceed_budget(sender, instance, created, **kwargs):
    if created:

        total_expenses = sum(
            expense.actual_amount if expense.actual_amount else 0
            for expense in Expense.objects.filter(trip_participation=instance.trip_participation)
        )

        declared_budget = instance.trip_participation.declared_budget
        if total_expenses > declared_budget:
            content = NotificationContent(
                message="notifications.content.expenses-exceed-budget",
                data={
                    "tripName": instance.trip_participation.trip.trip_name,
                    "totalExpenses": float(total_expenses),
                    "budget": float(declared_budget),
                    "tripId": instance.trip_participation.trip.trip_id
                }
            )

            notification = Notification.objects.create(
                user=instance.trip_participation.user,
                type="Budget",
                content=str(content),
                is_read=False,
                created_at=timezone.now()
            )
            notification.save()
    print(f"Notified user {instance.trip_participation.user} about expenses exceeding budget for "
          f"trip {instance.trip_participation.trip.trip_name} after adding Expense: {instance.expense_id}")


########################################################################################################################
@receiver(post_save, sender=TripInvitation)
def notify_trip_invitation_received(sender, instance, created, **kwargs):
    if created:
        content = NotificationContent(
            message="notifications.content.invitation-received",
            data={
                "tripName": instance.trip.trip_name,
                "alias": instance.sender.alias,
            }
        )

        notification = Notification.objects.create(
            user=instance.receiver,
            type="InvitationReceived",
            content=str(content),
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()
    print(f"Notified user {instance.receiver} about trip invitation for trip {instance.trip.trip_name}")


@receiver(post_save, sender=TripInvitation)
def notify_trip_invitation_accepted(sender, instance, created, **kwargs):
    if not created and instance.status == TripInvitation.TripInvitationStatus.ACCEPTED:
        content = NotificationContent(
            message="notifications.content.invitation-accepted",
            data={
                "tripName": instance.trip.trip_name,
                "alias": instance.receiver.alias,
                "tripId": instance.trip.trip_id
            }
        )

        notification = Notification.objects.create(
            user=instance.sender,
            type="InvitationAccepted",
            content=str(content),
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()
    print(f"Notified user {instance.sender} about trip invitation acceptance for trip {instance.trip.trip_name}")


@receiver(post_save, sender=TripInvitation)
def notify_trip_invitation_declined(sender, instance, created, **kwargs):
    if not created and instance.status == TripInvitation.TripInvitationStatus.DECLINED:
        content = NotificationContent(
            message="notifications.content.invitation-declined",
            data={
                "tripName": instance.trip.trip_name,
                "alias": instance.receiver.alias,
                "tripId": instance.trip.trip_id
            }
        )

        notification = Notification.objects.create(
            user=instance.sender,
            type="InvitationDeclined",
            content=str(content),
            is_read=False,
            created_at=timezone.now()
        )
        notification.save()
    print(f"Notified user {instance.sender} about trip invitation decline for trip {instance.trip.trip_name}")


########################################################################################################################

# Add here functions for creating notifications for other events : Keep in mind that the function should be decorated
# with @receiver(post_save, sender=ModelName) and the arguments should be (sender, instance, created, **kwargs)
# The function should create a Notification object and save it to the database
# The type of the notification should be "Info" or "Budget" or "Invitation"
# You are free to add more types if needed but make sure to update the frontend accordingly

########################################################################################################################
