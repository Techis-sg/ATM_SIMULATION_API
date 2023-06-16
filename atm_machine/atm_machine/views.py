
from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ParseError
from atm.serializers import ObtainTokenSerializer
from atm.serializers import AuthenticateCard
from .custom_auth_backend import JWTAuthentication
from accounts.models import Account
from atm.models import Card

User = get_user_model()

class ObtainTokenView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        card_number = serializer.validated_data.get('card_number')
        pin = serializer.validated_data.get('pin')

        dbcard = Card.objects.filter(card_number=card_number).first()
        print("\n dbcard ", dbcard)
        if dbcard is None:
            return Response({'message': 'Card not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            dbcardwithpin = Card.objects.filter(card_number=card_number, pin=pin).first()
            if dbcardwithpin is None:
                return Response({'message': 'Incorrect pin'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("\n dbcard.account.account_id  ", dbcard.account.account_id)
                account = Account.objects.filter(account_id=dbcard.account.account_id).first()
                print("\n account ", account)
                user = account.user
                print("\n user  ", user)
            card_details = {
                "card_number":dbcardwithpin.card_number,
                "pin":dbcardwithpin.pin,
            }

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user,card_details)

        return Response({'token': jwt_token})


# from django.contrib.auth import get_user_model
# from atm.models import Card
# from rest_framework.views import APIView
# from rest_framework.generics import RetrieveAPIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import serializers
# from rest_framework import status
# from atm.serializers import TokenSerializer
# from .custom_auth_backend import CustomAuthBackend

# from rest_framework_simplejwt.tokens import RefreshToken


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Card
#         fields = ('card_number', 'pin')


# class UserAPIView(RetrieveAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
    
#     def get_object(self):
#         return self.request.user
    

# # class CustomAuthView(APIView):
# #     def post(self, request):
# #         card_number = request.data.get('card_number')
# #         pin = request.data.get('pin')
        
# #         # Authenticate the user using the custom backend
# #         user = CustomAuthBackend().authenticate(request, card_number, pin)
# #         if not user:
# #             return Response({'error': 'Invalid card number or pin.'}, status=status.HTTP_401_UNAUTHORIZED)
        
# #         # Generate the JWT token
# #         refresh = RefreshToken.for_user(user)
        
# #         # Return the token to the client
# #         serializer = TokenSerializer({'refresh': str(refresh), 'access': str(refresh.access_token)})
# #         return Response(serializer.data, status=status.HTTP_200_OK)


# from rest_framework import generics, status
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from atm.models import Card
# from atm.serializers import CardSerializer,AuthenticateCard,TokenSerializer
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken


# class CustomAuthView(generics.CreateAPIView):
#     serializer_class = AuthenticateCard
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         card_number = serializer.validated_data['card_number']
#         pin = serializer.validated_data['pin']

#         # Custom authentication
#         user = authenticate(request=request, card_number=card_number, pin=pin)

#         if user is None:
#             return Response({'error': 'Invalid card number or PIN.'}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)
#         token = str(refresh.access_token)

#         return Response({'token': token}, status=status.HTTP_200_OK)
