from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def initial(self, request, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_staff:
            return self.permission_denied(request)

        return super(UserListCreateView,self).initial(request, *args, **kwargs)

    def permission_denied(self, request):
        return Response(
            {"error": "Forbidden request"},
            status=status.HTTP_403_FORBIDDEN
        )

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def initial(self, request, *args, **kwargs):
        # Check if the user is an admin
        if not request.user.is_staff:
            return self.permission_denied(request)

        return super(UserRetrieveUpdateDestroyView,self).initial(request, *args, **kwargs)

    def permission_denied(self, request):
        return Response(
            {"error": "Forbidden request"},
            status=status.HTTP_403_FORBIDDEN
        )
