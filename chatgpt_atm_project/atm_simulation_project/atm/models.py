from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Account(models.Model):
    account_id = models.IntegerField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Account"


class Card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='cards')
    number = models.CharField(max_length=16, unique=True)
    pin = models.CharField(max_length=4)

    def __str__(self):
        return f"Card: {self.number}"


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.transaction_type} - {self.amount}"
