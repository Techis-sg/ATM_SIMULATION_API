from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('listusercreate/', UserListCreateView.as_view(), name='user-list-create'),
    path('getuser/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),
]
