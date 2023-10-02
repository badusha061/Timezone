from django.shortcuts import render
from product.models import Product
# Create your views here.

from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html' )

def shop(request):
    product = Product.objects.all().order_by('-product_price')
    context = {
        'product':product
    }
    print('sized ',product)
    return render(request, 'home/shop.html',context)

def product_details(request):
    return render(request, 'home/product_details.html')

def blog(request):
    return render (request,'home/blog.html' )

def contact(request):
    return render(request, 'home/contact.html')
