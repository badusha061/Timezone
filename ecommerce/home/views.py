from django.shortcuts import render
from product.models import Product
from  categories.models import Brand
from offer.models import Offer
from product.models import Product
from categories.models import Category , Brand
from django.http import JsonResponse
from django.template.loader import render_to_string
from order.models import *
from userprofile.models import Address
from coupon.models import CouponUsage
from offer.models import Offer
from django.core import serializers
from banner.models import Banner
# Create your views here.

from django.shortcuts import render

# Create your views here.

def index(request):
    banner = Banner.objects.all() 

    context = {
        'banner':banner
    }
    return render(request, 'home/index.html',context)

def about(request):
    return render(request, 'home/about.html' )

def shop(request):
    product = Product.objects.all().order_by('-product_price')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'product':product,
        'categories':categories,
        'brands':brands
    }
    return render(request, 'home/shop.html',context)

def product_details(request):
    return render(request, 'home/product_details.html')

def blog(request):
    return render (request,'home/blog.html' )

def contact(request):
    return render(request, 'home/contact.html')



def invoice(request,invoice_id):
    order = Order.objects.get(id = invoice_id)
    order_item = OrderItem.objects.get(order_id = invoice_id)
    try:
        offer = order_item.product.product_brand.offer.discount_amount
    except AttributeError:
        try:
            offer = order_item.product.offer.discount_amount
        except AttributeError:
            offer = None

    
    discount_item = CouponUsage.objects.filter(user = request.user).first()
    if discount_item:
        discount = discount_item.discount_amount
    else:
        discount = None


    
    context = {
        'order':order,
        'order_item':order_item,
        'offer':offer,
        'discount':discount
    }
    return render(request,'user/invoice.html',context)



def search(request):
    if request.method == 'GET':
        quary = request.GET.get('q')
        products = Product.objects.filter(product_name__icontains = quary)
        context = {
            'product':products,
        }
        return render(request, 'home/shop.html',context)
    

def filter_category(request):
    if request.method == 'POST':
        products = Product.objects.all().order_by('id').distinct()

        categories = request.POST.getlist('category[]')
        if categories:
            print('the categories if condion is workings')
            product = products.filter(product_category__id__in = categories).distinct()

        brand = request.POST.getlist('brand[]')
        print('the brand is the',brand)
        if brand:
            print('the brand if condion workings')  
            product = products.filter(product_brand__id__in = brand).distinct()
        print('the product is the',product)
        context = {
            'product':product
        }
        return render(request,'home/shop.html',context)