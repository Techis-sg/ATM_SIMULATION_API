# from django.contrib import admin
# from accounts.models import User
# # Register your models here.

# admin.site.register(User)

from django.contrib import admin
from accounts.models import User,Account
# Register your models here.
    
admin.site.register([User,Account])