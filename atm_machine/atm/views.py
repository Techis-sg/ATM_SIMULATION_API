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
import os,sys

class CardCreateView(generics.CreateAPIView):
    serializer_class = CardSerializer


class CardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]


class UserFunctionalityViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def balance_inquiry(self, request, pk=None):
        """
        Get the balance of the account associated with a card.
        """
        try:
            card = get_object_or_404(Card, card_number=pk)
            account = card.account
            # serializer = AccountSerializer(account)
            return Response({"name":str(account.user.first_name)+' '+str(account.user.last_name),"card":card.card_number,"balance":account.balance},status=200)
            # return Response(serializer.data)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logMessage = "Exception in balance inquiry %s*****%s*****%s"%(str(exc_type),str(fname),str(exc_tb.tb_lineno))
            print(logMessage)
            return Response({"error":"Something went wrong"},status=500)

    @action(detail=True, methods=['POST'])
    def cash_withdrawal(self, request, pk=None):
        """
        Withdraw cash from the account associated with a card.
        """
        try:
            card = get_object_or_404(Card, card_number=pk)
            account = card.account
            account.balance = int(account.balance)
            withdrawal_amount = int(request.data.get('amount'))
            if withdrawal_amount < 0:
                return Response({'error': 'Invalid input'}, status=400)

            if account.balance >= withdrawal_amount:
                account.balance -= withdrawal_amount
                account.save()
                transaction = Transaction.objects.create(
                    account=account,
                    amount=withdrawal_amount,
                    actiontype='Debit'
                )
                serializer = TransactionSerializer(transaction)
                return Response({"message":"Acccount debited successfully","card":card.card_number,"remaining balance":account.balance,"transaction details ":serializer.data},status=200)
                # serializer = TransactionSerializer(transaction)
                # return Response(serializer.data)
            else:
                return Response({'error': 'Insufficient balance'}, status=400)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logMessage = "Exception in cash withdrawal %s*****%s*****%s"%(str(exc_type),str(fname),str(exc_tb.tb_lineno))
            print(logMessage)
            return Response({"error":"Something went wrong"},status=500)

    @action(detail=True, methods=['POST'])
    def cash_deposit(self, request, pk=None):
        """
        Deposit cash to the account associated with a card.
        """
        try:
            card = get_object_or_404(Card, card_number=pk)
            account = card.account
            deposit_amount = int(request.data.get('amount'))
            if deposit_amount < 0 :
                return Response({"error":'Invalid input'}, status=400)
            account.balance = int(account.balance)
            account.balance += deposit_amount
            account.save()
            transaction = Transaction.objects.create(
                account=account,
                amount=deposit_amount,
                actiontype='Credit'
            )
            serializer = TransactionSerializer(transaction)
            return Response({"message":"Account credited successfully","card":card.card_number,"new balance":account.balance,"transaction details ":serializer.data},status=200)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logMessage = "Exception in cash deposit %s*****%s*****%s"%(str(exc_type),str(fname),str(exc_tb.tb_lineno))
            print(logMessage)
            return Response({"error":"Something went wrong"},status=500)

    @action(detail=True, methods=['POST'])
    def change_pin(self, request, pk=None):
        """
        Change the PIN associated with a card.
        """
        try:
            card = get_object_or_404(Card, card_number=pk)
            serializer = ChangePinSerializer(data=request.data)

            if serializer.is_valid():
                old_pin = serializer.validated_data['old_pin']
                dbcard = Card.objects.filter(card_number=pk,pin=old_pin).first()
                if dbcard is None:
                    return Response({'error': 'Bad request. Incorrect details entered'},status=400)
                new_pin = serializer.validated_data['new_pin']
                card.pin = new_pin
                card.save()
                return Response({'message': 'PIN changed successfully'},status=200)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logMessage = "Exception in change pin %s*****%s*****%s"%(str(exc_type),str(fname),str(exc_tb.tb_lineno))
            print(logMessage)
            return Response({"error":"Something went wrong"},status=500)
