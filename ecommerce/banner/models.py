from django.db import models
from categories.models import Category
# Create your models here.

class Banner(models.Model):
    banner = models.CharField( max_length=50)
    banner_image = models.ImageField( upload_to='banner/', default='No image is available')
    caption = models.TextField()
    category_id = models.ForeignKey(Category,  on_delete=models.SET_NULL, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.banner

