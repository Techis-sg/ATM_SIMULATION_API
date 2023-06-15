"""
URL configuration for atm_machine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import ObtainTokenView
# from .views import CustomAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/accounts/', include('accounts.urls')),
    # path('api/atm/', include('atm.urls')),
    # path('api/transactions/', include('transactions.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('atm.urls')),
    path('api/', include('transactions.urls')),
    # path('api/authenticate/', UserAPIView.as_view(),name='authentication'),
    # path('api/auth/', CustomAuthView.as_view(), name='custom-auth'),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
