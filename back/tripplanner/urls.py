from django.urls import path
from authentication.views import LoginView, LogoutView, RegisterView
from core.views import CurrentUserView

urlpatterns = [
    path('api/auth/login', LoginView.as_view(), name='Login'),
    path('api/auth/logout', LogoutView.as_view(), name='Logout'),
    path('api/auth/register', RegisterView.as_view(), name='Register'),
    path('api/me', CurrentUserView.as_view(), name='CurrentUser'),
]
