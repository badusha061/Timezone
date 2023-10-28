from django.shortcuts import render , redirect
from django.contrib import messages
from product.models import Product ,ProductImage
from django.http.response import JsonResponse
from .models import Cart
from coupon.models import Coupon , CouponUsage
from django.db.models import Sum , F
from decimal import Decimal , ROUND_DOWN

# Create your views here.

def cart(request):
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).order_by('id')
            image_item = ProductImage.objects.filter(is_available = True).first()
            total_qty  = Sum(item.product.product_quantity for item in cart)

            
            grand_total = 0
            total_price = 0
            for item in cart:
                product_price = item.product.product_price
                product_offer = item.product.offer
                brand_offer = item.product.product_brand.offer

                if product_offer is  None and brand_offer is None:
                    total_price  += product_price * item.quantity
                else:
                    if product_offer and brand_offer:
                        disount = max(product_offer.discount_amount , brand_offer.discount_amount)
                    elif product_offer:
                        disount = product_offer.discount_amount
                    else:
                        disount = brand_offer.discount_amount
                    disount_price = (disount/100)*product_price
                    disount_amount = product_price - disount_price
                    total_price += disount_amount * item.quantity 
                grand_total = total_price
                item.total_price = total_price
                item.save()
            coupon = Coupon.objects.all()
            coupon_usage = CouponUsage.objects.filter(user = request.user)
            disount_percentage = None
            after_discount = None
            for i in coupon_usage:
                disount_percentage = i.discount_amount
                after_discount = i.total_price
            cart_itme = Cart.objects.filter(user = request.user)
            all_cart_item = not any( item.product.product_quantity <= 0 for item in cart_itme)
            
            context = {
                'cart': cart,
                'image_item' : image_item,
                'total_price':total_price,
                'grand_total':grand_total,
                'coupon':coupon,
                'discount': disount_percentage,
                'after_discount':after_discount,
                'total_qty':total_qty,
                'all_cart_item':all_cart_item
                
            }
            
            return render(request, 'home/cart.html', context)
        else:
            
            messages.error(request,'please Login')
            return redirect('userauth:user_login')
    except Exception as e:
        print(e)
        return redirect('userauth:user_login')

def add_cart(request ):
    try:
        if request.method == 'POST': 
            if request.user.is_authenticated:
                prod_id = request.POST.get('product_id')
                quantity = int(request.POST.get('product_count'))


                # validatings product here or not
                check_product = Product.objects.get(id = prod_id)
                

                #if check the prodcut is already exists or not 
                if Cart.objects.filter(user= request.user , product_id = prod_id).exists():
                    messages.error(request, 'product already existed in the cart')
                    return redirect('cart')
                    
                else:
                    product_qty = quantity

                    #create the product 
                    if check_product.product_quantity >= int(product_qty):
                        product_price = check_product.product_price 
                        product_offer = check_product.offer
                        brand_offer = check_product.product_brand.offer
                        if product_offer and brand_offer:
                            disocunt = max(product_offer.discount_amount,brand_offer.discount_amount)
                        elif product_offer:
                            disocunt = product_offer.discount_amount
                        elif brand_offer:
                            disocunt = brand_offer.discount_amount
                        else:
                            disocunt = 0
                        max_discout = (disocunt/100)*product_price
                        after = product_price - max_discout
                        cart_obj =  Cart.objects.create(user=request.user,product_id = prod_id,quantity = product_qty ,total_price = after , single_total = after )
                        cart_obj.save()
                        messages.success(request,'Product Added Successfully')
                        return redirect('cart')
                    else:
                        messages.error(request , 'Only Few Quanttity available')
                        return redirect('home:shop')

            else:
                messages.error(request ,'please login')
                return redirect('userauth:user_login')

        return render(request , 'home/shop.html')
    except Exception as e:
        print(e)
        return render(request, 'home/shop.html')


def update_cart(request):
    try:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            product_id = int(product_id)
            action = request.POST.get('action')

            if Cart.objects.filter(user=request.user,product_id = product_id).exists():
                product_qty = request.POST.get('quantity')
                if product_qty == '0':
                    status = ('zero qty not allowed')

                    return JsonResponse({"status":status , "product_qty":product_qty})
                product_qty = int(product_qty)
                product_id = request.POST.get('product_id')

                cart_item = Cart.objects.filter(product_id = product_id).first()
                if cart_item:    
                    if product_qty > cart_item.product.product_quantity:
                        status = ("Requested quantity exceeds available quantity")
                        return JsonResponse({"status":status})
                    else:
                        cart_it = Cart.objects.filter(user = request.user , product_id = product_id)
                        cart_items = Cart.objects.filter(product_id = product_id , user = request.user)
                        for cart_item in cart_items:
                            if product_qty > 0:
                                cart_item.quantity = product_qty
                                cart_item.save()
                            single_price = 0
                            total = 0
                            for item in cart_it:
                                product_price = item.product.product_price
                                brand_offer  = item.product.product_brand.offer
                                product_offer = item.product.offer
                                if product_offer and brand_offer:
                                    max_discount =  max(product_offer.discount_amount, brand_offer.discount_amount)
                                elif product_offer:
                                    max_discount = product_offer.discount_amount
                                elif brand_offer:
                                    max_discount = brand_offer.discount_amount
                                else:
                                    max_discount = 0
                                discount = Decimal((max_discount/100)*product_price)
                                discount = discount.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
                                
                                discount_price = product_price - discount
                                single_price = discount_price * item.quantity 
                                it = Cart.objects.filter(user = request.user)
                                total = 0
                                grand_total = {}
    
                                for i in it:
                                    if action == 'increment':
                                        i.total_price +=  Decimal(discount_price)
                                    elif action == 'decrement':
                                        i.total_price -= Decimal(discount_price) 
                                    i.save()
                                    grand_total[i.id] = i.total_price
                                    max_id =  max(grand_total)
                                status = ("Cart Updated Successfully")
                            return JsonResponse ({"status":status,"single_price":single_price,"total":item.total_price , "total":total })
                else:
                    status = ("No matching product found in cart")
                    return JsonResponse({"status":status})
            else:
                messages.error(request, 'Product does not exits')
                return redirect('cart')
    except Exception as e:
        print(e)
        return redirect('cart')




def delete_cart(request,delete_id):
    try:
        if request.method == 'POST':
            dele = Cart.objects.filter(id = delete_id)
            delete = CouponUsage.objects.filter(user = request.user)
            delete.delete()
            dele.delete()
            messages.success(request, 'Successfully Deleted')
            return redirect('cart')
        else:
            messages.error(request , 'please login')
            return redirect('userauth:user_login')
    except Exception as e:
        print(e)
        return redirect('cart')