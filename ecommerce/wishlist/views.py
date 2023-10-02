from django.shortcuts import render , redirect
from .models import Wishlist
from django.http import JsonResponse
from django.contrib import messages
# Create your views here.

def wishlist(request):
    if request.user.is_authenticated:
        product = Wishlist.objects.filter(user = request.user)
        context = {
            'product':product
        }
        return render(request , 'wishlist/wishlist.html',context)
    else:
        messages.error(request, 'please login')
        return redirect('userauth:user_login')

def add_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            if Wishlist.objects.filter(user = request.user ,  product_id = product_id).exists():
                print('already exited')
                return JsonResponse({'status': 'Product already in Wishlist'})
            else:
                print('suiiiiiiiiiiiiii')
                Wishlist.objects.create(user = request.user , product_id = product_id)
                return JsonResponse({'status':'Product added successfully in Wishlist'})
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})
    else:
        return redirect('home:home')
        

def delete_wishlist(request , deletewishlist_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            dele = Wishlist.objects.get(id = deletewishlist_id)
            dele.delete()
            messages.success(request , 'Successfully Deleted')
            return redirect('wishlist')   
        else:
            messages.error(request, 'please login')
            return redirect('userauth:user_login')