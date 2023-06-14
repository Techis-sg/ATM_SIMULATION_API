from django.db import models
from accounts.models import Account
from datetime import datetime
current_time=datetime.now()
# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    actiontype = models.CharField(max_length=2, choices=(('C','Credit'),('D','Debit')), default='C')
    timestamp = models.DateTimeField(default=current_time.strftime("%G-%m-%d %H:%M:%S"))
    
    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f'{self.account} | {self.amount} | {formatted_timestamp}'
    
    class Meta:
        db_table = 'transaction'
        managed = True
