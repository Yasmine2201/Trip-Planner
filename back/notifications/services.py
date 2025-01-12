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
        return notification

    @staticmethod
    def set_read_user_notification(user: User, notification_id: int):
        """
        Set a specific notification associated with a user as read.
        """

        notification = Notification.objects.get(user=user.user_id, notification_id=notification_id)
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

    # ## used for tests only
    # @staticmethod
    # def create_notification(user: User, payload : dict):
    #     """
    #     Create a notification for a user.
    #     """
    #     print("Service", user, type(user))
    #     print("Service", user.user_id, type(user.user_id))
    #     notification = Notification.objects.create(user=user, **payload)
    #     notification.save()
    #     return notification

