from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Card
from .serializers import CardSerializer


class CardCreateView(generics.CreateAPIView):
    serializer_class = CardSerializer


class CardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]
