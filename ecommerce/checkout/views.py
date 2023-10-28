from django.shortcuts import render , redirect
from .models import Order , OrderItem
from cart.models import Cart
from userprofile.models import Address , Wallet
from django.contrib import messages
from coupon.models import Coupon , CouponUsage
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.http import HttpResponse 
from product.models import Product
import random
import re
from django.core.validators import validate_email
from django.forms import ValidationError

# Create your views here.

def checkout(request):
    try:
        cart_item = Cart.objects.filter(user = request.user)
        if cart_item:
            address_item = Address.objects.filter(user=request.user)
            coupon = Coupon.objects.all()
            coupon_usage = CouponUsage.objects.filter(user = request.user)

            total = 0
            for item in cart_item:
                print(item.total_price)
                total = item.total_price
            if coupon_usage:
                for item in coupon_usage:
                    print(item.total_price)
                    total = item.total_price
            
            context = {
                'cart_items':cart_item,
                'total':total,
                'address_item':address_item,
                'coupon':coupon,
                'coupon_usage' : coupon_usage,
            }
            return render(request,'home/checkout.html',context)
        else:
            return render(request,'home/checkout.html')
    except Exception as e:
        print(e)
        return render(request,'home/checkout.html')



def add_address_check(request):
    try:
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
            if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),number):
                messages.error(request,'Enter valid phone number')
                return redirect('userprofile')
            phonenumber_checkings = len(number)
            if not phonenumber_checkings == 10:
                messages.error(request, 'Phone Number should be 10 digits')
                return redirect('userprofile')
            
            if email.strip() == '':
                messages.error(request, 'Email feild is empty')
                return redirect('add_address_check')
            email_check = validator_email(email)
            if email_check is False:
                messages.error(request, 'Email is not valid')
                return redirect('userprofile')
            
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
            
            if not re.search(re.compile(r'^\d{6}$'),pincode):
                messages.error(request,'Should only 6 contain numeric')
                return redirect('userprofile')

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
    except Exception as e:
        print(e)
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
    try:
        if request.method == 'POST':
            coupon = request.POST['coupon_code']
            grand_total_string = request.POST['grand_total'].replace('$', '').strip()

            grand_total = float(grand_total_string)
            print('the grand total is the ',grand_total)
            try:
                coupon_code = Coupon.objects.get(coupon_code = coupon)
            except Coupon.DoesNotExist:
                return JsonResponse({'message':'Coupon does not exist'})
            if grand_total > coupon_code.min_price:
                if  CouponUsage.objects.filter( user = request.user).exists():
                    print('already taken')
                    return JsonResponse({"message":"Coupon already used!"})    
                discount = grand_total * coupon_code.discount / 100
                print('the grand total is the',discount)
                grand_total = grand_total- ((coupon_code.discount /100)*grand_total)
                usercoupon = CouponUsage.objects.create(user = request.user , coupon = coupon_code , used = True , total_price = grand_total , discount_amount = discount)
                usercoupon_data = serializers.serialize('python', [usercoupon])[0]
                usercoupon.save()
                print('the discount amount is the ',discount)
                print('the grand totol is the ',grand_total)
                return JsonResponse({
                    'message': 'Coupon added successfully',
                    'usercoupon': usercoupon_data,
                    'grand_total':grand_total,
                    'discount':discount,

                })

            else:
                return JsonResponse({'message':'You are not eligible for this coupon'})                    
        return redirect('checkout')
    except Exception as e:
        print(e)
        return render(request,'home/checkout.html')


def placeorder(request):
    try:
        if request.method == 'POST':
            user = request.user
            user_name = User.objects.get(username =user)
            address_id = request.POST.get('address') 

            if address_id is None:
                messages.error(request, 'Address should be take')
                return redirect('checkout') 
            
            address = Address.objects.get(id = address_id)     

            payment_mode = request.POST.get('payment-method') 
            payment_id = request.POST.get('payment_id')
            cart = Cart.objects.filter(user = request.user)
            
            total =  0 
            coupon_usege = CouponUsage.objects.filter(user = request.user) 
            if coupon_usege:               
                for i in coupon_usege:
                    total = i.total_price
            else:
                for item in cart:
                    total = item.total_price
                    

            if payment_mode == 'wallet':
                wallet_qs = Wallet.objects.filter(user=request.user)
                if not wallet_qs.exists():
                    data = "No Wallet found for the user"
                    return JsonResponse({"status": data})

                wallet_instance = wallet_qs.first()
                wallet_balance = wallet_instance.wallet

                if total > wallet_balance:
                    data = 'You Do Not Have Sufficient Balance'
                    return JsonResponse({"status": data})

                
                wallet_instance.wallet = wallet_balance - total
                wallet_instance.save()
    
            

            if payment_mode == 'cod' or 'paypal' or 'wallet':
                order_item = Order.objects.create(
                    user = user_name,
                    address = address,
                    payment_mode = payment_mode,
                    total_price = total,
                    payment_id = payment_id,
                    tracking_no = generate_tracking()
                
                )
                order_item.save()
                print('saved data')
                messages.success(request , 'Succesfully order')
            

            
            cart_item = Cart.objects.filter(user = user_name)
            for item in cart_item:
                product = item.product
                product.product_quantity -= item.quantity
                product.save()
                item = OrderItem.objects.create(
                    order = order_item,
                    product = item.product,
                    price = total,
                    quantity = item.quantity,
                    user = user_name
                )
            item.save() 
            messages.success(request, 'Order has been placed')
            if payment_mode == 'paypal' or 'cod' or 'wallet':
                return JsonResponse({'status':'Order has been placed'})
            return redirect('home:invoice')


        return render(request,'home/checkout.html') 
    except Exception as e:
        print(e)
        return render(request,'home/checkout.html')





# razorpay

def rezorpaycheck(request):
    cart = Cart.objects.filter(user = request.user)
    for item in cart:
        total_price = item.total_price * item.quantity
    return JsonResponse({'total_price':total_price})


# generate tracking  number
def generate_tracking():
    track_no = random.randint(1111111, 9999999)

    while Order.objects.filter(tracking_no=track_no).exists():
        track_no = random.randint(1111111, 9999999)
    return track_no



def validator_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False