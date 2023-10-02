from django.shortcuts import render , redirect
from django.contrib import messages
from product.models import Product ,ProductImage
from django.http.response import JsonResponse
from .models import Cart
# Create your views here.

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('id')
        image_item = ProductImage.objects.filter(is_available = True).first()
       

        total_price = 0
        for item in cart:
            item.total_price = item.product.product_price * item.quantity
            total_price += item.total_price 
            item.save()
        
        context = {
            'cart': cart,
            'total_price':total_price,
            'image_item' : image_item
             
        }
        
        return render(request, 'home/cart.html', context)
    else:
        
        messages.error(request,'please Login')
        return redirect('userauth:user_login')


def add_cart(request ):
    if request.method == 'POST': 
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            quantity = int(request.POST.get('product_count'))


            # validatings product here or not
            check_product = Product.objects.get(id = prod_id)
            

            #if check the prodcut is already exists or not 
            if Cart.objects.filter(user= request.user , product_id = prod_id).exists():
                messages.error(request, 'product already existed in the cart')
                print('already existed')
                return redirect('cart')
                
            else:
                product_qty = quantity

                #create the product 
                if check_product.product_quantity >= int(product_qty):
                    Cart.objects.create(user=request.user,product_id = prod_id,quantity = product_qty)
                    messages.success(request,'Product Added Successfully')
                    return redirect('cart')
                else:
                    messages.error(request , 'Only Few Quanttity available')
                    return redirect('home:shop')

        else:
            messages.error(request ,'please login')
            return redirect('userauth:user_login')

    return render(request , 'home/shop.html')


def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if Cart.objects.filter(user=request.user, product_id=product_id).exists():
            product_qty = int(request.POST.get('product_count'))
            product_id = request.POST.get('product_id')
            product_total = request.POST.get('product_total')

            
            cart_item = Cart.objects.get(user = request.user , product_id = product_id)
                
            if product_qty > cart_item.product.product_quantity:
                messages.error(request, 'Requested quantity exceeds available quantity')
                return redirect('cart')
            else:
                Cart.objects.filter(user = request.user , product_id = product_id).update(quantity = product_qty, total_price = product_total)

                cart = Cart.objects.get(user=request.user, product_id = product_id)
                totalprice = cart.total_price
                data = {
                    'message': 'Product quantity updated successfully',
                    'total': totalprice, 
                }
                return JsonResponse(data)

        else:
            messages.error(request, 'Product does not exits')
            return redirect('cart')




def delete_cart(request,delete_id):
    if request.method == 'POST':
        dele = Cart.objects.filter(id = delete_id)
        dele.delete()
        messages.success(request, 'Successfully Deleted')
        return redirect('cart')
    else:
        messages.error(request , 'please login')
        return redirect('userauth:user_login')