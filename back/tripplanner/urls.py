from django.urls import path
from back.authentication.views import LoginView, LogoutView, RegisterView

urlpatterns = [
    path('api/auth/login', LoginView.as_view(), name='Login'),
    path('api/auth/logout', LogoutView.as_view(), name='Logout'),
    path('api/auth/register', RegisterView.as_view(), name='Register'),
]
