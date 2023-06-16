from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Card
from .serializers import CardSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Card
from accounts.models import Account
from transactions.models import Transaction
from .serializers import (
    CardSerializer,
    AccountSerializer,
    TransactionSerializer,
    ChangePinSerializer,
)
from atm_machine.custom_auth_backend import JWTAuthentication
import decimal



class CardCreateView(generics.CreateAPIView):
    serializer_class = CardSerializer


class CardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]


class UserFunctionalityViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def balance_inquiry(self, request, pk=None):
        """
        Get the balance of the account associated with a card.
        """
        card = get_object_or_404(Card, card_number=request.card)
        account = card.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cash_withdrawal(self, request, pk=None):
        """
        Withdraw cash from the account associated with a card.
        """
        card = get_object_or_404(Card, card_number=request.card)
        account = card.account
        withdrawal_amount = decimal.Decimal(request.data.get('amount'))


        if account.balance >= withdrawal_amount:
            account.balance -= withdrawal_amount
            account.save()
            transaction = Transaction.objects.create(
                account=account,
                amount=withdrawal_amount,
                actiontype='D'
            )
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        else:
            return Response({'error': 'Insufficient funds'}, status=400)

    @action(detail=True, methods=['post'])
    def cash_deposit(self, request, pk=None):
        """
        Deposit cash to the account associated with a card.
        """
        card = get_object_or_404(Card, card_number=request.card)
        account = card.account
        deposit_amount = decimal.Decimal(request.data.get('amount'))

        account.balance += deposit_amount
        account.save()
        transaction = Transaction.objects.create(
            account=account,
            amount=deposit_amount,
            actiontype='C'
        )
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=['post'])
    def change_pin(self, request, pk=None):
        """
        Change the PIN associated with a card.
        """
        card = get_object_or_404(Card, card_number=request.card)
        serializer = ChangePinSerializer(data=request.data)

        if serializer.is_valid():
            new_pin = serializer.validated_data['pin']
            card.pin = new_pin
            card.save()
            return Response({'message': 'PIN changed successfully'})
        else:
            return Response(serializer.errors, status=400)
