from django.urls import path

from authentication.views import LoginView, LogoutView, RegisterView
from notifications.views import NotificationView
from core.views import CurrentUserView, OtherUsersView
from trips.views import TripView, LastTripView

urlpatterns = [
    path('api/auth/login', LoginView.as_view(), name='Login'),
    path('api/auth/logout', LogoutView.as_view(), name='Logout'),
    path('api/auth/register', RegisterView.as_view(), name='Register'),
    path('api/me', CurrentUserView.as_view(), name='CurrentUser'),

    path('api/users', OtherUsersView.as_view(), name='OtherUsers'),
    path('api/users/<str:user_id>', OtherUsersView.as_view(), name='OtherUsers'),

    path('api/trips', TripView.as_view(), name='trip-view'),
    path('api/trips/<int:trip_id>', TripView.as_view(), name='trip-view'),
    path('api/trips/last', LastTripView.as_view(), name='trip-view'),

    path('api/notifications', NotificationView.as_view(), name='notification-view'),
    path('api/notifications/<int:notification_id>', NotificationView.as_view(), name='notification-view'),
]
