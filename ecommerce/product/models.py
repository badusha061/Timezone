from django.db import models
from categories.models import Brand , Category
# Create your models here.


class Product(models.Model):
    product_name = models.CharField( unique=True,max_length=50)
    product_price = models.IntegerField()
    product_brand = models.ForeignKey(Brand,  on_delete=models.CASCADE , null=True)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(upload_to='product_image', default='NO image is available' , null=True , blank=True)
    product_quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField( upload_to='product_image',blank=True,default=True,null=True, height_field=None, width_field=None, max_length=None)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Image for {'self.product.product_name'}"



