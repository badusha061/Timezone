from django.shortcuts import render , redirect
from .models import Coupon , CouponUsage
from django.contrib import messages
import re
from django.utils import timezone
from datetime import datetime
# Create your views here.

def coupon(request):  
    try:
        coupon_item = Coupon.objects.all()
        context = {
            'coupon_item':coupon_item,
        }   
        return render(request,'coupon/coupon.html',context)
    except Exception as e:
        print(e)
        return render(request, 'coupon/coupon.html')
    
def add_coupon(request):
    try:
        if request.method == 'POST':
            coupon_name = request.POST['coupon']
            coupon_code = request.POST['coupon_code']
            coupon_discount = request.POST['discount']
            minimum_price = request.POST['min_price']
            start_date_s = request.POST['valid_from']
            end_date_s = request.POST['valid_to']
            print('the min price is the', minimum_price)
            if coupon_name.strip() == '':
                messages.error(request, 'Name fields is empty')
                return redirect('coupon')
            if not re.search(r'\b[A-Z0-9a-z]{2,}\b', coupon_code):
                messages.error(request,'Coupon code must be letter and numbers')
                return redirect('coupon')
            if coupon_discount.strip() == '':
                messages.error(request, 'Dicount fields is empty')
                return redirect('coupon')
            # m = int(minimum_price)
            # if m > 0:
            #     messages.error(request, 'the price should be greater than zero')
            #     return redirect('coupon')
            if minimum_price.strip() == '':
                messages.error(request, 'price feilds is empty')
                return redirect('coupon')
            try:
                start_date = datetime.strptime(start_date_s, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_s,'%Y-%m-%d').date()
            except ValueError:
                messages.error(request,'invalid date format . Use YYYY-MM-DD.')
                return redirect('coupon')
            if start_date >= end_date:
                messages.error(request, 'Start date must be before the end date')
                return redirect('coupon')
            if start_date < timezone.now().date():
                messages.error(request, "Start date cannot be in the past.")
                return redirect('coupon')
            print(coupon_name,coupon_code,coupon_discount,minimum_price,start_date_s ,end_date_s)
            coupon_item = Coupon.objects.create(
                coupon_name = coupon_name,
                coupon_code = coupon_code,
                discount = coupon_discount,
                min_price = minimum_price,
                start_date = start_date_s,
                end_date = end_date_s)
            coupon_item.save()
            messages.success(request, 'Successfully Added')
            return redirect('coupon')        
        return render(request,'coupon/coupon.html')
    except Exception as e:
        print(e)
        return render(request,'coupon/coupon.html')



def edit_coupon(request,editcoupon_id):
    try:
        if request.method == 'POST':
            coupon_name = request.POST['coupon']
            coupon_code = request.POST['coupon_code']
            coupon_discount = request.POST['discount']
            minimum_price = request.POST['min_price']
            start_date_s = request.POST['valid_from']
            end_date_s = request.POST['valid_to']
            

            if coupon_name.strip() == '':
                messages.error(request, 'Name fields is empty')
                return redirect('coupon')
            if not re.search(r'\b[A-Z0-9a-z]{2,}\b', coupon_code):
                messages.error(request,'Coupon code must be letter and numbers')
                return redirect('coupon')
            if coupon_discount.strip() == '':
                messages.error(request, 'Dicount fields is empty')
                return redirect('coupon')
            m = int(minimum_price)
            if m>0:
                messages.error(request, 'the price should be greater than zero')
                return redirect('coupon')
            if minimum_price.strip() == '':
                messages.error(request, 'price feilds is empty')
                return redirect('coupon')
            try:
                start_date = datetime.strptime(start_date_s, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_s,'%Y-%m-%d').date()
            except ValueError:
                messages.error(request,'invalid date format . Use YYYY-MM-DD.')
                return redirect('coupon')
            if start_date >= end_date:
                messages.error(request, 'Start date must be before the end date')
                return redirect('coupon')
            if start_date < timezone.now().date():
                messages.error(request, "Start date cannot be in the past.")
                return redirect('coupon')



            coupon_item = Coupon.objects.create(id = editcoupon_id)
            coupon_item.coupon_name = coupon_name
            coupon_item.coupon_code = coupon_code
            coupon_item.discount = coupon_discount
            coupon_item.min_price = minimum_price
            coupon_item.start_date = start_date_s
            coupon_item.end_date = end_date_s

            messages.success(request, 'Successfully Edited')
            coupon_item.save()
            return render(request,'coupon/coupon.html')
        
        return render(request, 'coupon/coupon.html')
    except Exception as e:
        print(e)
        return render(request,'coupon/coupon.html')


def delete_coupon(request,deletecoupon_id):
    try:
        if request.method == 'POST':
            dele = Coupon.objects.get(id = deletecoupon_id)
            dele.delete()
            messages.success(request, 'Successfully deleted')
            return redirect('coupon')
    except Exception as e:
        print(e)
        return render(request,'coupon/coupon.html')
    
def  search_coupon(request):
    return render(request,'coupon/coupon.html' )



