from django.urls import path
from .views import CardCreateView, CardRetrieveUpdateDestroyView,UserFunctionalityViewSet

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'users', UserFunctionalityViewSet, basename='userfunc')

urlpatterns = [
    path('cards/', CardCreateView.as_view(), name='card-create'),
    path('cards/<int:pk>/', CardRetrieveUpdateDestroyView.as_view(), name='card-retrieve-update-destroy'),
    # User URLs
    # path('users/<int:pk>/balance/', UserFunctionalityViewSet.as_view(), name='balance-inquiry'),
    # path('users/<int:pk>/withdraw/', UserFunctionalityViewSet.as_view(), name='cash-withdrawal'),
    # path('users/<int:pk>/deposit/', UserFunctionalityViewSet.as_view(), name='cash-deposit'),
    # path('users/<int:pk>/change-pin/', UserFunctionalityViewSet.as_view(), name='change-pin'),
] + router.urls

