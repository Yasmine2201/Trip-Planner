from django.urls import path

from authentication.views import LoginView, LogoutView, RegisterView
from budget.views import BudgetView, ExpenseView, ExpenseShareView, CategoryView
from notifications.views import NotificationView
from core.views import CurrentUserView, OtherUsersView
from trips.views import TripView, LastTripView, TripSentInvitation
from visits.views import VisitView, LocationView


urlpatterns = [
    # Authentication
    path('api/auth/login', LoginView.as_view(), name='Login'),
    path('api/auth/logout', LogoutView.as_view(), name='Logout'),
    path('api/auth/register', RegisterView.as_view(), name='Register'),

    # Profile
    path('api/me', CurrentUserView.as_view(), name='CurrentUser'),

    path('api/users', OtherUsersView.as_view(), name='OtherUsers'),
    path('api/users/<str:user_id>', OtherUsersView.as_view(), name='OtherUsers'),

    # Trips
    path('api/trips', TripView.as_view(), name='trip-view'),
    path('api/trips/<int:trip_id>', TripView.as_view(), name='trip-view'),
    path('api/trips/last', LastTripView.as_view(), name='trip-view'),

    # Trip Invitations
    #path('api/trips/<int:trip_id>/invitations', TripView.as_view(), name='trip-view'),
    path('api/trips/<int:trip_id>/invitations/', TripSentInvitation.as_view(), name='trip-invitation-view'),
    path('api/trips/<int:trip_id>/invitations/<int:invitation_id>', TripSentInvitation.as_view(), name='trip-invitation-view'),

    # Notifications

    path('api/notifications', NotificationView.as_view(), name='notification-view'),
    path('api/notifications/<int:notification_id>', NotificationView.as_view(), name='notification-view'),

    # Budget and expenses
    path('api/trips/<int:trip_id>/budget', BudgetView.as_view(), name='budget-view'),
    path('api/trips/<int:trip_id>/budget/expenses', ExpenseView.as_view(), name='expense-view'),
    path('api/trips/<int:trip_id>/budget/expenses/<int:expense_id>', ExpenseView.as_view(), name='expense-view'),

    # Categories
    path('api/categories', CategoryView.as_view(), name='category-view'),

    # Expense sharing
    path('api/trips/<int:trip_id>/budget/expenses/share', ExpenseShareView.as_view(), name='expense-share-view'),
    path('api/trips/<int:trip_id>/budget/expenses/share/<int:share_id>', ExpenseShareView.as_view(),
         name='expense-share-view'),
    path('api/trips/<int:trip_id>/budget/expenses/share/debts', ExpenseShareView.as_view(), name='expense-share-view'),
    path('api/trips/<int:trip_id>/budget/expenses/share/refunds', ExpenseShareView.as_view(), name='expense-share-view'),

    # Visits
    path('api/trips/<int:trip_id>/visits', VisitView.as_view(), name='visit-view'),
    path('api/trips/<int:trip_id>/visits/<int:visit_id>', VisitView.as_view(), name='visit-view'),

    # Locations
    path('api/locations', LocationView.as_view(), name='location-view'),
]
