from django.shortcuts import render , redirect
from categories.models import Brand , Category
from .models import Product  , ProductImage
from django.contrib import messages 
from django.db.models import Q
from offer.models import Offer
# Create your views here.


def product_list(request):
    try:
        product = Product.objects.filter(is_available = True).order_by('id')
        brand = Brand.objects.filter(is_available = True).order_by('id')
        image = ProductImage.objects.filter(is_available = True).order_by('id')
        category = Category.objects.filter(is_available = True).order_by('id')
        offer = Offer.objects.filter(is_available = True).order_by('id')
        context = {
            'product':product,
            'brand':brand,  
            'image':image,
            'category':category,
            'offer':offer
        }

        return render(request, 'product/product.html',context)
    except Exception as e:
        print(e)
        return render(request, 'product/product.html')


def add_product(request):
    try:
        if request.method == 'POST':
            name = request.POST['product_name']
            price = request.POST['product_price']
            images  = request.FILES.getlist('product_image')
            brand_id = request.POST.get('product_brand')
            catgory_id = request.POST.get('product_category')
            quantity = request.POST.get('product_quantity')
            offer = request.POST.get('offer')

            # validatings the fields is empty
            if name.strip() == '' or price.strip() == '' or quantity.strip() == '':
                messages.error(request, 'feilds is empty')
                return redirect('add_product')
            if brand_id.strip() == '':
                messages.error(request,'field is empty')
            if catgory_id.strip() == '':
                messages.error(request, 'Category is field is empty')
            if Product.objects.filter(product_name = name).exists():
                messages.error(request, 'the product name is already taken')
                return redirect('add_product')  
            print('the image is the',images[0])
            # add product
            brand = Brand.objects.get(id = brand_id)
            category = Category.objects.get(id = catgory_id)
            product = Product(
                product_name = name,
                product_price = price,
                product_brand = brand,
                product_quantity = quantity,
                product_category = category,
                offer_id = offer,

                product_image = images[0]
            )
            product.save()
            for image in images:
                product_image = ProductImage(product=product, image = image)
                product_image.save()

            messages.success(request, ' successfully added')
    
        return redirect('product_list')
    except Exception as e:
        print(e)
        return redirect('product_list')


def search_product(request):
    try:
        if request.method == 'POST':
            search = request.POST['search']

            #validatings the fields is empty
            if search.strip() == '':
                messages.error(request, 'the field is empty')
                return redirect('search_product')
            product = Product.objects.filter(Q(product_name__icontains = search)|Q(product_price__icontains = search)|Q(product_quantity__icontains = search)|Q(product_brand__brand_name__icontains = search),is_available =True)
            context = {
                'product':product,
                'brand':Brand.objects.filter(is_available = True).order_by('id')
            }
            if product:
                pass
                return render(request, 'product/product.html' , context)
            else:
                messages.error(request, 'search not found')
                return redirect('product_list')
        return render(request, 'product/product.html')
    except Exception as e:
        print(e)
        return render(request,'product/product.html')

def delete_product(request,deleteproduct_id):
    try:
        dele = Product.objects.get(id = deleteproduct_id)
        dele.delete()
        return redirect('product_list')
    except Exception as e:
        print(e)
        return redirect('product_list')


def edit_product(request,editproduct_id):
    try:
        if request.method == 'POST':
            name = request.POST['product_name']
            price = request.POST['product_price']
            brand_id = request.POST.get('product_brand')
            quantity = request.POST.get('product_quantity')
            offer = request.POST.get('offer')
            print('the offer is the ',offer)
            product_categories = request.POST.get('product_category')

            #validatings the fields is empty
            if name.strip() == '':
                messages.error(request, 'Product name feilds is empty')
                return redirect('product_list')
            if price.strip() == '':
                messages.error(request, 'Product price is empty')
                return redirect('product_list')
            if quantity.strip() == '':
                messages.error(request, 'Product quantity feilds is empty')
                return redirect('product_list')
            
            #validatings the image is empty
            try:
                images = request.FILES.getlist('product_image')
                product = Product.objects.get(id = editproduct_id)
                if images:           
                    for image in images:
                        product_image = ProductImage(product=product,image = image)
                        product_image.save()                
            except Product.DoesNotExist:
                messages.error(request, 'image not found')

            
            #editings the product 
            product = Product.objects.get(id = editproduct_id)
            brand = Brand.objects.filter(brand_name = brand_id)
            if offer:
                offer_obj = Offer.objects.get(id = offer)
            else:
                offer_obj = None

            if product_categories:
                category_ob = Category.objects.get(id = product_categories)
            else:
                category_ob = None
            product.product_name = name
            product.product_price = price
            product.product_brand.brand_name = brand
            product.product_quantity = quantity
            product.offer = offer_obj
            product.product_category = category_ob
            product.save()
            messages.success(request, 'successfully edited')

        return render(request , 'category/category.html')
    except Exception as e:
        print(e)
        return render(request, 'category/category.html')


def product_view(request, viewproduct_id):
 
    # getings the products and returings the indivual product
    product = Product.objects.get(id = viewproduct_id)
    brand = Brand.objects.filter(is_available = True).order_by('id')
    category = Category.objects.filter(is_available = True).order_by('id')
    image_prodcut = ProductImage.objects.filter(product=product.id)

    
    context = {
        'product':product,
        'brand':brand,
        'category':category,
        'image_product':image_prodcut
    }
    return render(request , 'home/product_details.html' , context)


def adminpage(request):
    return redirect('adminside:dashboard')

def product_details(request,product_id):
    product = Product.objects.get(id = product_id)
    product_image = ProductImage.objects.filter(product = product_id) 
    if product:        
        context = {
            'product':product,
            'product_image':product_image
        }
        return render(request,'product/product_show.html',context)
    else:
        messages.error(request,'Not product found')
        return redirect('home:shop')
    

