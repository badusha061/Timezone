from django.db import models
from product.models import Product , ProductImage
from django.contrib.auth.models import User
from decimal import Decimal
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False , null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    single_total = models.IntegerField()
    created_at = models.DateField( auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username