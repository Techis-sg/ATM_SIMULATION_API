from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Card, Account, Transaction
from .serializers import (
    UserSerializer,
    CardSerializer,
    AccountSerializer,
    TransactionSerializer,
    ChangePinSerializer
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.settings import api_settings
import jwt
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import TokenSerializer
from .models import Card, User
from .authentication_backends import JWTAuthentication


class UserListView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CardListView(ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]


class CardDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAdminUser]


class AccountListView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUser]


class AccountDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminUser]


class TransactionListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]


class TransactionDetailView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAdminUser]


class ObtainTokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print("\n inside post")
        card_number = serializer.validated_data.get('cardnumber')
        pin = serializer.validated_data.get('pin')

        dbcard = Card.objects.filter(number=card_number).first()
        print("\n dbcard ", dbcard)
        if dbcard is None:
            return Response({'message': 'Card not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            dbcardwithpin = Card.objects.filter(number=card_number, pin=pin).first()
            if dbcardwithpin is None:
                return Response({'message': 'Incorrect pin'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("\n dbcard.account.account_id  ", dbcard.account.account_id)
                account = Account.objects.filter(account_id=dbcard.account.account_id).first()
                print("\n account ", account)
                user = account.user
                print("\n user  ", user)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token})


class UserFunctionalityView(APIView):
    permission_classes = []

    def get(self, request, pk=None):
        """
        Get the balance of the account associated with a card.
        """
        card = Card.objects.get(number=pk)
        account = card.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def post(self, request, pk=None):
        """
        Withdraw cash from the account associated with a card.
        """
        card = Card.objects.get(number=pk)
        account = card.account
        withdrawal_amount = request.data.get('amount')

        if account.balance >= withdrawal_amount:
            account.balance -= withdrawal_amount
            account.save()
            transaction = Transaction.objects.create(
                account=account,
                amount=withdrawal_amount,
                transaction_type='Withdrawal'
            )
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        else:
            return Response({'error': 'Insufficient funds'}, status=400)

    def put(self, request, pk=None):
        """
        Deposit cash to the account associated with a card.
        """
        card = Card.objects.get(number=pk)
        account = card.account
        deposit_amount = request.data.get('amount')

        account.balance += deposit_amount
        account.save()
        transaction = Transaction.objects.create(
            account=account,
            amount=deposit_amount,
            transaction_type='Deposit'
        )
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=201)

    def patch(self, request, pk=None):
        """
        Change the PIN associated with a card.
        """
        card = Card.objects.get(number=pk)
        serializer = ChangePinSerializer(data=request.data)

        if serializer.is_valid():
            new_pin = serializer.validated_data['pin']
            card.pin = new_pin
            card.save()
            return Response({'message': 'PIN changed successfully'})
        else:
            return Response(serializer.errors, status=400)
