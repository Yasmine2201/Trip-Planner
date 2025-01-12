from rest_framework.response import Response

from authentication.utils import ProtectableAPIView, TokenAuthentication
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from notifications.services import NotificationService


# Create your views here.

class NotificationView(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request, notification_id=None):
        """
        Fetch all notifications associated with a user or a specific notification.
        If a notification_id is provided, fetch the specific notification and set it as read if it is not already.
        """
        user = request.user

        if notification_id:
            try:
                notification = NotificationService.get_user_notification(user, notification_id)
                return Response(NotificationSerializer(notification).data, status=200)
            except Notification.DoesNotExist:
                return Response({"error": "Notifications not found"}, status=404)
        else:
            notifications = NotificationService.get_all_user_notifications(user).order_by('-created_at')
            if not notifications:
                return Response({"error": "No notifications found"}, status=404)
            return Response(NotificationSerializer(notifications, many=True).data)

    @staticmethod
    def put(request, notification_id):
        """
        Set a specific notification associated with a user as read.
        """
        user = request.user
        try:
            notification = NotificationService.set_read_user_notification(user, notification_id)
            return Response(NotificationSerializer(notification).data, status=200)
        except Notification.DoesNotExist:
            return Response({"error": "Notifications not found"}, status=404)

    @staticmethod
    def delete(request, notification_id):
        """
        Delete a specific notification associated with a user.
        """
        user = request.user
        try:
            notification = NotificationService.delete_user_notification(user, notification_id)
            return Response({f'notification {notification} has been deleted successfully'}, status=200)

        except Notification.DoesNotExist:
            return Response({"error": "Notifications not found"}, status=404)

    ### used for tests only
    # @staticmethod
    # def post (request):
    #     """
    #     Create a notification for a user.
    #     """
    #     user = request.user
    #     print("View", user, type(user))
    #     payload = request.data
    #     notification = NotificationService.create_notification(user, payload)
    #     return Response(NotificationSerializer(notification).data, status=201)
