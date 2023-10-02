
from django.contrib import admin
from .models import OrderReturn , OrderCancel

# Register your models here.
admin.site.register(OrderReturn)
admin.site.register(OrderCancel)