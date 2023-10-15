from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    first_name = models.CharField( max_length=50,blank=True)
    last_name = models.CharField( max_length=50,blank=True)
    phone = models.CharField(blank=True, max_length=50)
    email = models.EmailField( max_length=254,blank=True)
    address = models.CharField( max_length=50,blank=True)
    country = models.CharField( max_length=50,blank=True)
    state = models.CharField( max_length=50,blank=True)
    city = models.CharField( max_length=50,blank=True)
    pincode = models.CharField( max_length=50,blank=True)
    order_note = models.CharField( max_length=50,null=True, default='')
    is_available = models.BooleanField(null=True,blank=True,default=True)
    image = models.ImageField( upload_to='userprofile',null=True,blank=True, height_field=None, width_field=None, max_length=None)

    def __str__(self) -> str:
        return f"{self.id}"
    


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet = models.PositiveIntegerField(default=0)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,null=True)
    RAZORPAY = 'Razorpay'
    COD = 'COD'
    WALLET = 'Wallet'
    TRANSACTION_METHOD_CHOICES = [
        (RAZORPAY, 'Razorpay'),
        (COD, 'Cash on Delivery'),
        (WALLET, 'Wallet')  
    ]
    CANCEL_ORDER = 'Cancel Order'
    RETURN_ORDER = 'Return Order'
    TRANSACTION_REASONS = [
        (CANCEL_ORDER, 'Cancel Order'),
        (RETURN_ORDER, 'Return Order'),
    ]
    reason = models.CharField(max_length=20, choices=TRANSACTION_REASONS,null=True)
    payment_method = models.CharField( max_length=50,choices=TRANSACTION_METHOD_CHOICES, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)    
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)