from django.contrib import admin
from .models import Address , Wallet , Transaction
# Register your models here.

admin.site.register(Address)
admin.site.register(Wallet)
admin.site.register(Transaction)