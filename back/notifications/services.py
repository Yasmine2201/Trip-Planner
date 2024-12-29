from core.models import User
from notifications.models import Notification


class NotificationService:

    @staticmethod
    def get_all_user_notifications(user: User):
        """
        Fetch all notifications associated with a user.
        """

        return Notification.objects.filter(user=user.user_id)

    @staticmethod
    def get_user_notification(user: User, notification_id: int):
        """
        Fetch a specific notification associated with a user and set it as read.
        """

        notification = Notification.objects.get(user=user.user_id, notification_id=notification_id)
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return notification

    @staticmethod
    def delete_user_notification(user: User, notification_id: int):
        """
        Delete a specific notification associated with a user.
        """

        notification = Notification.objects.get(user=user.user_id, notification_id=notification_id)
        notification.delete()
        return notification

