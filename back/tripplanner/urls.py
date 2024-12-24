from django.urls import path, include

from authentication.views import LoginView, LogoutView, RegisterView

from core.views import CurrentUserView
from trips.views import TripView, LastTripView

urlpatterns = [
    path('api/auth/login', LoginView.as_view(), name='Login'),
    path('api/auth/logout', LogoutView.as_view(), name='Logout'),
    path('api/auth/register', RegisterView.as_view(), name='Register'),
    path('api/me', CurrentUserView.as_view(), name='CurrentUser'),

    path('api/trips', TripView.as_view(), name='trip-view'),
    path('api/trips/<int:trip_id>', TripView.as_view(), name='trip-view'),
    path('api/trips/last', LastTripView.as_view(), name='trip-view'),
]
