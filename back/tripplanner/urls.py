from django.urls import path, include
from rest_framework.routers import DefaultRouter

from authentication.views import LoginView, LogoutView, RegisterView

from core.views import CurrentUserView
from trips.views import TripView

urlpatterns = [
    path('api/auth/login', LoginView.as_view(), name='Login'),
    path('api/auth/logout', LogoutView.as_view(), name='Logout'),
    path('api/auth/register', RegisterView.as_view(), name='Register'),
    path('api/me', CurrentUserView.as_view(), name='CurrentUser'),

    path('api/trips', TripView.as_view(), name='trip-list')
]
