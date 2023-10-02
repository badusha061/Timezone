from django.shortcuts import render , redirect
from checkout.models import Order , OrderItem
from userprofile.models import Address
from product.models import ProductImage
from django.contrib import messages
# Create your views here.

def admin_order(request):
    order_item = Order.objects.all()
   
    context = {
        
        'order_item':order_item
    }
    return render(request,'adminside/order.html',context)


def user_order(request):
   
    order_details = OrderItem.objects.filter(user = request.user)
    order_item = Order.objects.filter(user = request.user)

 
    context = {
        
        'order_datails':order_details,
        'order_item':order_item,
    }
    return render(request,'user/userorder.html',context)


def order_views(request):
    order_views = OrderItem.objects.filter(user = request.user)
    order = Order.objects.filter(user = request.user)
    address = Address.objects.filter(user = request.user)
    context = {
        'order_views':order_views,
        'order':order,
        'address':address
    }
    
    return render(request , 'order/orderview.html',context)


def order_views_admin(request,orderviews_id):
    order_views = OrderItem.objects.filter(user = request.user)
    order = Order.objects.filter(id = orderviews_id)
    address = Address.objects.filter(user = request.user)
    for item in order:
        print(item.od_status)
    context = {
        'order_views':order_views,
        'order':order,
        'address':address
    }
    
    return render(request, 'adminside/orderview.html', context)


def change_status(request):
    if request.method == 'POST':
        order_item = request.POST.get('orderitem_id')
        status = request.POST.get('status')
        order_item = OrderItem.objects.get(id = order_item )
        order_item.status = status
        order_item.save()
        messages.success(request, 'Successfully updated ')
        return redirect('admin_order')
    return render(request, 'adminside/orderview.html')
