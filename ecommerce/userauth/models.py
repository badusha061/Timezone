from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Customer(User):
    gender = models.CharField(max_length=10)
    otp = models.IntegerField(blank=True , null= True , default= True)
    timme_st = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.username