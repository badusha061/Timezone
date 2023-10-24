from django.db import models
from django.contrib.auth.models import User
from userprofile.models import Address
from product.models import Product
from datetime import timedelta
# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True)
    total_price = models.IntegerField(null=True) 
    payment_mode = models.CharField( max_length=50,default=True)
    payment_id = models.CharField( max_length=50,blank=True,null=True,default=True)
    messages = models.TextField(blank=True,null=True,default=True)
    tracking_no =models.CharField( max_length=50,default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    orderstatuses = {
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return', 'Return')       
    }
    od_status = models.CharField( max_length=150 , default='pending',choices=orderstatuses , null=True)
    @property
    def expected_delivery(self):
        return self.created_at + timedelta(days=7)

    def __str__(self):
        return f"{self.id, self.user.username}"
    
class  OrderItem(models.Model):
    user = models.ForeignKey( User,on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product =models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    orderstatuses = {
        ('Pending','Pending'),
        ('Processing','Processing'),
        ('Shipped','Shipped'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Return', 'Return')       
    }
    status = models.CharField(choices=orderstatuses, max_length=150,default='pendings')

    def __str__(self) -> str:
        return self.user.username
