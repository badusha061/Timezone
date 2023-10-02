from django.db import models
from product.models import Product , ProductImage
from django.contrib.auth.models import User
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False , null=False)
    total_price = models.IntegerField(blank=True , null=True)
    created_at = models.DateField( auto_now_add=True)

    