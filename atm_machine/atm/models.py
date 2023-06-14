from django.db import models
from accounts.models import Account

# Create your models here.

class Card(models.Model):
    card_number = models.CharField(max_length=19,primary_key=True)
    pin = models.IntegerField()
    is_blocked = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.card_number}"
    
    class Meta:
        db_table = 'card'
        managed = True
