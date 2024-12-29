from time import sleep

from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework.response import Response

from authentication.utils import ProtectableAPIView, TokenAuthentication
from core.services import UserService
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from notifications.services import NotificationService
from notifications.utils import event_stream


# Create your views here.
class NotificationSSE(ProtectableAPIView):
    authentication_classes = [TokenAuthentication]
    @staticmethod
    def get(request):
        user_id = request.user.user_id
        response = StreamingHttpResponse(event_stream(user_id), content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response

class NotificationView(ProtectableAPIView):
    """
    Offers two functionalities:
    - Fetch all notifications associated with a user or a specific notification if a notification_id is provided.
    - Delete a specific notification associated with a user.
    """

    authentication_classes = [TokenAuthentication]

    @staticmethod
    def get(request, notification_id = None):
        """
        Fetch all notifications associated with a user or a specific notification.
        If a notification_id is provided, fetch the specific notification and set it as read if it is not already.
        """
        user = request.user

        if notification_id:
            try :
                notification = NotificationService.get_user_notification(user, notification_id)
                return Response(NotificationSerializer(notification).data, status=200)
            except Notification.DoesNotExist:
                return Response({"error": "Notification not found"}, status=404)
        else :
                notifications = NotificationService.get_all_user_notifications(user)
                if not notifications:
                    return Response({"error": "No notifications found"}, status=404)
                return Response(NotificationSerializer(notifications, many=True).data)

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
            return Response({"error": "Notification not found"}, status=404)











