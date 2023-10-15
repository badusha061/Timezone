from django.db import models
from checkout.models import Order , OrderItem
from django.contrib.auth.models import User
# Create your models here.

class OrderReturn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    option = models.CharField(max_length=50)
    reason = models.TextField()

    def __str__(self) -> str:
        return self.user.username
    

class OrderCancel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    option = models.CharField( max_length=50,null=True)
    reason = models.TextField(null=True)

    def __str__(self) -> str:
        return self.user.username