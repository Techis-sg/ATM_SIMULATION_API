from django.urls import path
from .views import CardCreateView, CardRetrieveUpdateDestroyView

urlpatterns = [
    path('cards/', CardCreateView.as_view(), name='card-create'),
    path('cards/<int:pk>/', CardRetrieveUpdateDestroyView.as_view(), name='card-retrieve-update-destroy'),
]
