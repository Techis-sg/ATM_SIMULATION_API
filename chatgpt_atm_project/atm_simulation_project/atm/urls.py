from django.urls import path
from .views import (
    UserListView,
    UserDetailView,
    CardListView,
    CardDetailView,
    AccountListView,
    AccountDetailView,
    TransactionListView,
    TransactionDetailView,
    UserFunctionalityView,
    ObtainTokenView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Admin URLs
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('admin/cards/', CardListView.as_view(), name='card-list'),
    path('admin/cards/<int:pk>/', CardDetailView.as_view(), name='card-detail'),
    path('admin/accounts/', AccountListView.as_view(), name='account-list'),
    path('admin/accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('admin/transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('admin/transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),

    # User URLs
    path('users/token/', ObtainTokenView.as_view(), name='obtain-token'),
    path('users/refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('users/<int:pk>/balance/', UserFunctionalityView.as_view(), name='balance-inquiry'),
    path('users/<int:pk>/withdraw/', UserFunctionalityView.as_view(), name='cash-withdrawal'),
    path('users/<int:pk>/deposit/', UserFunctionalityView.as_view(), name='cash-deposit'),
    path('users/<int:pk>/change-pin/', UserFunctionalityView.as_view(), name='change-pin'),
]
