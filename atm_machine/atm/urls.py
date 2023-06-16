from django.urls import path
from .views import CardCreateView, CardRetrieveUpdateDestroyView
from .views import UserFunctionalityViewSet

balance_inquiry = UserFunctionalityViewSet.as_view({
    'get': 'balance_inquiry',
})
cash_withdrawal = UserFunctionalityViewSet.as_view({
    'post': 'cash_withdrawal',
})
cash_deposit = UserFunctionalityViewSet.as_view({
    'post': 'cash_deposit',
})



urlpatterns = [
    path('cards/', CardCreateView.as_view(), name='card-create'),
    path('cards/<int:pk>/', CardRetrieveUpdateDestroyView.as_view(), name='card-retrieve-update-destroy'),
    path('balance_inquiry/', balance_inquiry, name='balance_inquiry'),
    path('cash_withdrawal/', cash_withdrawal, name='cash_withdrawal'),
        path('cash_deposit/', cash_deposit, name='cash_deposit'),



]
