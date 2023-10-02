from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(User ,   on_delete=models.CASCADE)
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