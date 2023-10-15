from django.db import models
from django.contrib.auth.models import User 
from userprofile.models import Address
# Create your models here.

class Customer(User):
    gender = models.CharField(max_length=10)
    otp = models.IntegerField(blank=True , null= True , default= True)
    timme_st = models.DateTimeField(auto_now=True)
    refferal_code = models.CharField(unique=True, max_length=50,null=True)
    referrer = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    images=models.ImageField(upload_to='photos/userprofile',blank=True)

    def __str__(self) -> str:
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=50)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username