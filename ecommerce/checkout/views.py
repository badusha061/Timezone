from django.shortcuts import render , redirect
from .models import Order , OrderItem
from cart.models import Cart
from userprofile.models import Address
from django.contrib import messages
from coupon.models import Coupon , CouponUsage
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse 

# Create your views here.

def checkout(request):
    cart_item = Cart.objects.filter(user = request.user)
    address_item = Address.objects.filter(user=request.user)
    coupon = Coupon.objects.all()
    total = 0
    for item in cart_item:
        total += item.total_price
    context = {
        'cart_item':cart_item,
        'total':total,
        'address_item':address_item,
        'coupon':coupon,
    }
    return render(request,'home/checkout.html',context)


def add_address_check(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        number = request.POST.get('phone')
        email = request.POST.get('email')
        address_user = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        order_note = request.POST.get('order_note')

                # validatings fields is empty
        if not request.user.is_authenticated:
            messages.error(request, 'User field must be login')
            return redirect('add_address_check')

        if firstname.strip() == '':
            messages.error(request , 'First name fiels is empty')
            return redirect('add_address_check')
        if lastname.strip() == '':  
            messages.error(request ,'Last name is empty')
            return redirect('add_address_check')
        if number.strip() == '':
            messages.error(request, 'Number feilds is empty')
            return redirect('add_address_check')
        if email.strip() == '':
            messages.error(request, 'Email feild is empty')
            return redirect('add_address_check')
        if address_user.strip() == '':
            messages.error(request , 'Address feilds is empty')
            return redirect('add_address_check')
        if country.strip() == '':
            messages.error(request, 'Country feild is empty')
            return redirect('add_address_check')
        if state.strip() == '':
            messages.error(request , 'State feild is empty')
            return redirect('add_address_check')
        if city.strip() == '':
            messages.error(request, 'City feilds is empty')
            return redirect('add_address_check')
        if pincode.strip() == '':
            messages.error(request , 'Pincode is empty')
            return redirect('add_address_check')

        #creatings address
        address_item = Address.objects.create(
            user = request.user,
            first_name = firstname,
            last_name = lastname,
            email = email,
            phone = number,
            address = address_user,
            country = country,
            state = state,
            city = city,
            pincode = pincode,
            order_note = order_note,
        )
  
       
        address_item.save()
        messages.success(request, 'Succesffully added')
        return redirect('checkout')
    return render(request,'home/checkout.html')



def edit_address_check(request,editaddres_id):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        number = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        order_note = request.POST.get('order_note')

        # validatings the fields is empty
        if request.user is None:
            messages.error(request, 'User field must be login')
            return redirect('edit_address_check')

        if firstname.strip() == '':
            messages.error(request , 'First name fiels is empty')
            return redirect('edit_address_check')
        if lastname.strip() == '':  
            messages.error(request ,'Last name is empty')
            return redirect('edit_address_check')
        if number.strip() == '':
            messages.error(request, 'Number feilds is empty')
            return redirect('edit_address_check')
        if email.strip() == '':
            messages.error(request, 'Email feild is empty')
            return redirect('edit_address_check')
        if address.strip() == '':
            messages.error(request , 'Address feilds is empty')
            return redirect('edit_address_check')
        if country.strip() == '':
            messages.error(request, 'Country feild is empty')
            return redirect('edit_address_check')
        if state.strip() == '':
            messages.error(request , 'State feild is empty')
            return redirect('edit_address_check')
        if city.strip() == '':
            messages.error(request, 'City feilds is empty')
            return redirect('edit_address_check')
        if pincode.strip() == '':
            messages.error(request , 'Pincode is empty')
            return redirect('edit_address_check')


        #Editings the address
        address = Address.objects.get(id = editaddres_id)

        address.first_name = firstname
        address.last_name = lastname
        address.phone = number
        address.email = email
        address.country = country
        address.state = state
        address.city = city
        address.pincode = pincode
        address.order_note = order_note
        address.save()
        return render(request,'home/checkout.html')
    

def apply_coupon(request):
    if request.method == 'POST':
        coupon = request.POST['coupon_code']
        grand_total = float(request.POST['grand_total'])    
        try:
            coupon_code = Coupon.objects.get(coupon_code = coupon)
        except Coupon.DoesNotExist:
            return JsonResponse({'message':'invalid coupon'})
        if grand_total > coupon_code.min_price:
            if  CouponUsage.objects.filter( user = request.user).exists():
                print('already taken')
                messages.error(request, 'Coupon is already taken ')
                return redirect('checkout')
            grand_total = grand_total - (grand_total*(coupon_code.discount /100))
            usercoupon = CouponUsage.objects.create(user = request.user , coupon = coupon_code , used = True , total_price = grand_total)
            usercoupon_data = serializers.serialize('python', [usercoupon])[0]
            usercoupon.save()
            messages.success(request, 'Coupon is successfully added')
            print('succcussfully saved')
            return JsonResponse({
                'message': 'Coupon added successfully',
                'usercoupon': usercoupon_data,
                'grand_total':grand_total,

            })

        else:
            return JsonResponse({'message':'You are not eligible for this coupon'})                    
    return redirect('checkout')


def placeorder(request):
    if request.method == 'POST':
        user = request.user
        user_name = User.objects.get(username =user)
        address_id = request.POST.get('default_address')    

        if address_id is None:
            messages.error(request, 'Address should be take')
            return redirect('checkout') 
        
        address = Address.objects.get(id = address_id)        

        payment_mode = request.POST.get('payment-method') 
        total =  0 
        coupon_usege = CouponUsage.objects.filter(user = request.user) 
        for i in coupon_usege:
            total = i.total_price
        if payment_mode == 'cod':
            order_item = Order.objects.create(
                user = user_name,
                address = address,
                payment_mode = payment_mode,
                total_price = total,
               
            )
            order_item.save()
            print('saved data')
            messages.success(request , 'Succesfully order')
        

        
        cart_item = Cart.objects.filter(user = user_name)
        for item in cart_item:
            item = OrderItem.objects.create(
                order = order_item,
                product = item.product,
                price = total,
                quantity = item.quantity,
                user = user_name
            )
        item.save()
        print('order item saved')
        return redirect('user_order')


    return render(request,'home/checkout.html') 







