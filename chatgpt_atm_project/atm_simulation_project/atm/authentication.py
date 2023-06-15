from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from .models import Card

User=get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = super().get_validated_token(request)

        if token is None:
            return None

        card_number = request.data.get('card_number')
        pin = request.data.get('pin')

        if not card_number or not pin:
            return None

        try:
            card = Card.objects.select_related('account__user').get(number=card_number)
        except Card.DoesNotExist:
            return None

        if not card.account.user.check_password(pin):
            return None

        user = User.objects.get(id=card.account.user.id)
        return user, token
