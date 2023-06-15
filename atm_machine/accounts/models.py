from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser): 
    class Meta:
        db_table = 'atmuser'
        managed = True


class Account(models.Model):
    account_id = models.IntegerField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Account {self.account_id}"
    
    class Meta:
        db_table = 'account'
        managed = True

