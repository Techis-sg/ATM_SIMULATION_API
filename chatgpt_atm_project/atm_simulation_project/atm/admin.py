from django.contrib import admin
from .models import Card, Account, Transaction, User

admin.site.register(Card)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(User)
