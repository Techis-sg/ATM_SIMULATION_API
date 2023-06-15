from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Card
User = get_user_model()


class CardAuthenticationBackend(BaseBackend):
    def authenticate(self, request, card_number=None, pin=None):
        try:
            card = Card.objects.get(card_number=card_number, pin=pin)
            user = card.user
            return user
        except ObjectDoesNotExist:
            return None


class CardTokenAuthentication(JWTAuthentication):
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
