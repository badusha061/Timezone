from django.shortcuts import render , redirect
from checkout.models import Order , OrderItem
from userprofile.models import Address , Transaction , Wallet
from product.models import ProductImage
from django.contrib import messages
from .models import OrderCancel , OrderReturn 
# Create your views here.

def admin_order(request):
    try:
        order_item = Order.objects.all()
    
        context = {
            
            'order_item':order_item
        }
        return render(request,'adminside/order.html',context)
    except Exception as e:
        print(e)
        return render(request, 'adminside/order.html')


def user_order(request):
    try:
        order_details = OrderItem.objects.filter(user = request.user)
        order_item = Order.objects.filter(user = request.user)
        for i in order_item:
            print(i.od_status)

    
        context = {
            
            'order_datails':order_details,
            'order_item':order_item,
        }
        return render(request,'user/userorder.html',context)
    except Exception as e:
        print(e)
        return render(request, 'user/userorder.html')

def order_views(request,orderviews_id):
    try:
        order = Order.objects.filter(id = orderviews_id)
        order_item = OrderItem.objects.filter(order_id = orderviews_id)
        print(order_item)
        context = {
            'order_views':order_item,
            'order':order,
        }
        
        return render(request , 'order/orderview.html',context)
    except Exception as e:
        print(e)
        return render(request, 'order/orderview.html')


def order_views_admin(request,orderviews_id):
    try:
        order_views = OrderItem.objects.filter(order_id = orderviews_id)
        order = Order.objects.filter(id = orderviews_id)


        context = {
            'order_views':order_views,
            'order':order,
        }
        
        return render(request, 'adminside/orderview.html', context)
    except Exception as e:
        print(e)
        return render(request, 'adminside/orderview.html')


def change_status(request):
    try:
        if request.method == 'POST':
            print('the function is calling',request.method)
            orderitem = request.POST.get('orderitem_id')
            status = request.POST.get('status')
            order_item = OrderItem.objects.get(id = orderitem )
            view_id = order_item.order.id
            order = Order.objects.get(id = view_id)
            order_item.status = status
            order.od_status = status
            order_item.save()
            order.save()
            messages.success(request, 'Successfully updated ')
            return redirect('admin_order')
        return render(request, 'adminside/orderview.html')
    except Exception as e:
        print(e)
        return render(request, 'adminside/orderview.html')


def cancel_order(request,ordercancel_id):
    try:
        order_id = OrderItem.objects.get(order_id = ordercancel_id)
        orderitem = order_id
        id = order_id.order.id
    except:
        return redirect('order_views')
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        option = request.POST.get('options')

        order_id = Order.objects.get(id = id)
        order_item = OrderItem.objects.get(order_id = ordercancel_id)
        qty = orderitem.quantity
        cancel = OrderCancel()
        cancel.user = request.user 
        cancel.order = order_id
        cancel.reason = reason
        cancel.option = option
        if order_id.payment_mode == 'cod':
            product = order_item.product
            product.product_quantity += order_item.quantity
            product.save()
            order_item.quantity = 0
            order_id.od_status = 'Cancelled'
            order_item.status = 'Cancelled' 
            
            order_item.save()
            order_id.save()
            cancel.save()
            print('saved both')
        elif order_id.payment_mode == 'paypal':
            wallet = Wallet.objects.filter(user  = request.user).first()
            if wallet:
                wallet.user = request.user
                wallet.wallet += order_id.total_price
                wallet.save()
            else:
                print('the else condion is working ')
                wallet = Wallet.objects.create(user = request.user , wallet = order_id.total_price)
                wallet.save()
            product = order_item.product
            product.product_quantity += order_item.quantity
            product.save()
            order_item.quantity = 0
            order_item.product.product_quantity += order_item.quantity
            order_id.od_status = 'Cancelled'
            order_item.status = 'Cancelled' 
            order_item.save()
            order_id.save()
            cancel.save()
            
            Transaction.objects.create(
                wallet = wallet,
                reason = 'Cancel Order',
                payment_method = 'Razorpay',
                amount = order_id.total_price,
                description = reason    
            )
            print('saved the transaction')
            messages.success(request, 'Successfully Added into Wallet')

    return redirect('user_order')


def return_order(request,orderreturn_id):
    try:
        order_id = OrderItem.objects.get(order_id = orderreturn_id)
        orderitem = order_id
        id = order_id.order.id
    except:
        return redirect('user_order')
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        option = request.POST.get('options')
        order = Order.objects.get(id = id )
        order_item = OrderItem.objects.get(order_id = orderreturn_id)
        qty = order_item.quantity
        return_order = OrderReturn()
        product = order_item.product
        product.product_quantity += order_item.quantity
        product.save()
        return_order.reason = reason
        return_order.option = option
        return_order.user = request.user
        return_order.order = order
        return_order.save()
        orderitem.status = 'Return'
        order.od_status = 'Return'
        order_item.save()
        order.save()
        print('saved')
        try:
            wallet = Wallet.objects.filter(user = request.user).first()
            wallet.user = request.user
            wallet.wallet += order.total_price
            wallet.save()
            messages.success(request,'Successfully Added to Wallet')
        except Exception as e:
            wallet = Wallet.objects.create(user = request.user ,wallet = order.total_price)
            wallet.save()
            messages.success(request,'Successfully Created Wallet')
        Transaction.objects.create(
            wallet = wallet,
            reason = 'Return Order',
            payment_method = order.payment_mode,
            amount = order.total_price,
            description = reason,
            )
        print('saved')
            

        messages.success(request, 'Successfully Returned')
        return redirect('user_order')
        


def order_tracker(request , ordertracker_id):
    try:
        track = Order.objects.get(id = ordertracker_id)
        context = {
            'track':track
        }
        print(track.od_status)
        return render(request,'order/ordertracker.html',context)
    except Exception as e:
        print(e)
        return render(request, 'order/ordertracker.html')