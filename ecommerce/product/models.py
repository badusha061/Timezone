from django.db import models
from categories.models import Brand , Category
from offer.models import Offer
# Create your models here.


class Product(models.Model):    
    from categories.models import Brand

    product_name = models.CharField( unique=True,max_length=50)
    product_price = models.IntegerField()
    product_brand = models.ForeignKey(Brand,  on_delete=models.CASCADE , null=True)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
    product_image = models.ImageField(upload_to='product_image', default='NO image is available' , null=True , blank=True)
    product_quantity = models.IntegerField()    
    is_available = models.BooleanField(default=True)
    offer =  models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True  )

    def __str__(self):
        return self.product_name
    


    def get_offer(self):
        product_offer = self.offer
        brand_offer = self.product_brand.offer
        if product_offer and brand_offer:

            # if both product and brand have the offer and take the max offer price 
            max_disount = max(product_offer.discount_amount,brand_offer.discount_amount)
            discount  = (max_disount/100)*self.product_price
            discount_amount = self.product_price - discount
            return discount_amount
        elif product_offer:
            #if product offer only have the offer 
            discount = (product_offer.discount_amount/100)*self.product_price
            discount_amount = self.product_price - discount
            return discount_amount
        elif brand_offer:
            # if brand offer only have the offer
            discount = (brand_offer.discount_amount/100)*self.product_price
            discount_amount =  self.product_price - discount
            return discount_amount
        else:
            return self.product_price

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField( upload_to='product_image',blank=True,default=True,null=True, height_field=None, width_field=None, max_length=None)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Image for {'self.product.product_name'}"
    





