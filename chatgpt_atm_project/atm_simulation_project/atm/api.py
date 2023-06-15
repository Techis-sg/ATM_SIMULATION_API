from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Card, Account, Transaction
from .serializers import (
    CardSerializer,
    AccountSerializer,
    TransactionSerializer,
    ChangePinSerializer,
)
from .authentication import CustomJWTAuthentication


class UserFunctionalityViewSet(viewsets.ViewSet):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def balance_inquiry(self, request, pk=None):
        """
        Get the balance of the account associated with a card.
        """
        card = get_object_or_404(Card, number=pk)
        account = card.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cash_withdrawal(self, request, pk=None):
        """
        Withdraw cash from the account associated with a card.
        """
        card = get_object_or_404(Card, number=pk)
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

    @action(detail=True, methods=['post'])
    def cash_deposit(self, request, pk=None):
        """
        Deposit cash to the account associated with a card.
        """
        card = get_object_or_404(Card, number=pk)
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

    @action(detail=True, methods=['post'])
    def change_pin(self, request, pk=None):
        """
        Change the PIN associated with a card.
        """
        card = get_object_or_404(Card, number=pk)
        serializer = ChangePinSerializer(data=request.data)

        if serializer.is_valid():
            new_pin = serializer.validated_data['pin']
            card.pin = new_pin
            card.save()
            return Response({'message': 'PIN changed successfully'})
        else:
            return Response(serializer.errors, status=400)
