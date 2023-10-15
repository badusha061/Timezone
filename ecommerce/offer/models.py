from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
'discount_amount','start_date','end_date'
# Create your models here.

class Offer(models.Model):
    offer_name = models.CharField(null=True, max_length=50)
    discount_amount = models.PositiveIntegerField()
    start_date =  models.DateField( default= timezone.now)
    end_date = models.DateField(default= timezone.now)
    is_available  = models.BooleanField(default=True)

 
    
    def is_offer_expired(self):
        return timezone.now().date() >= self.end_date

