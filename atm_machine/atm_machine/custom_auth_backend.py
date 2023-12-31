# from django.contrib.auth.backends import BaseBackend
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.exceptions import AuthenticationFailed


# class CustomAuthBackend(BaseBackend):
#     def authenticate(self, request, card_number=None, pin=None):
#         User = get_user_model()
#         try:
#             # Find the user based on the card number
#             user = User.objects.get(card_number=card_number)
#         except User.DoesNotExist:
#             raise AuthenticationFailed('Invalid card number or pin.')
        
#         # Check if the pin is correct
#         if not user.check_pin(pin):
#             raise AuthenticationFailed('Invalid card number or pin.')
        
#         # Authentication successful
#         return user


from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import Account
from atm.models import Card
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()

        # Get the user from the database
        card_number = payload.get('card_number')
        dbcard = Card.objects.filter(card_number=card_number).first()
        if dbcard is None:
            raise AuthenticationFailed('Card not found')
        else:
            account = Account.objects.filter(account_id=dbcard.account.account_id).first()
            user = account.user
            #adding user and transaction related information to request object
            request.card = dbcard
        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user, card_details):
        # Create the JWT payload
        payload = {
            'user_identifier': user.username,
            'exp': int((datetime.now() + settings.JWT_AUTH['JWT_EXPIRATION_DELTA']).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'username': user.username,
            "card_number":card_details.get("card_number"),
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token