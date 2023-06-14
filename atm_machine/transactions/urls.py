from django.urls import path
from .views import TransactionListCreateView, TransactionRetrieveView

urlpatterns = [
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveView.as_view(), name='transaction-retrieve'),
]
