from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Coupon(models.Model):
    coupon_name = models.CharField( max_length=50)
    coupon_code = models.CharField( max_length=50)
    discount = models.PositiveIntegerField()
    min_price = models.IntegerField()
    start_date = models.DateField( default=timezone.now)
    end_date = models.DateField( default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.coupon_name
    
    
    def is_coupon_expired(self):
        return timezone.now().date() >= self.end_date
    

class CouponUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    total_price = models.BigIntegerField()
    discount_amount  = models.BigIntegerField(blank=True, null=True)
    used = models.BooleanField()
    useage_date = models.DateField( auto_now=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.coupon .coupon_code}"
    