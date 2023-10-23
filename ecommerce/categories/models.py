from django.db import models
from offer.models import Offer

# Create your models here.

class Category(models.Model):
    name = models.CharField( max_length=50,blank=True , default=True , null=True)
    image = models.ImageField( upload_to='photos/name', height_field=None, width_field=None, max_length=None,default='No image available')
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name       ='Category'
        verbose_name_plural='name'

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    brand_name = models.CharField( max_length=50,blank=True,null=True)
    brand_image = models.ImageField( upload_to='brand/', height_field=None, width_field=None, max_length=None)
    brand_discription = models.TextField(max_length=200)
    is_available = models.BooleanField(default=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True )


    def __str__(self) -> str:
        return self.brand_name
    
    
    class Meta:
        verbose_name       ='Brand'
        verbose_name_plural='brand_name'
