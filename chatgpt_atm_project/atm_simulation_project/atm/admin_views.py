from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionHistoryView(APIView):
    def get(self, request):
        # Implement transaction history retrieval here
        # Retrieve all transactions and serialize them
        pass
