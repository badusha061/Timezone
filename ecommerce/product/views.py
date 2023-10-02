from django.shortcuts import render , redirect
from categories.models import Brand , Category
from .models import Product  , ProductImage
from django.contrib import messages 
from django.db.models import Q
# Create your views here.


def product_list(request):
    product = Product.objects.filter(is_available = True).order_by('id')
    brand = Brand.objects.filter(is_available = True).order_by('id')
    image = ProductImage.objects.filter(is_available = True).order_by('id')
    category = Category.objects.filter(is_available = True).order_by('id')
    context = {
        'product':product,
        'brand':brand,  
        'image':image,
        'category':category
    }

    return render(request, 'product/product.html',context)


def add_product(request):
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        images  = request.FILES.getlist('product_image')
        brand_id = request.POST.get('product_brand')
        catgory_id = request.POST.get('product_category')
        quantity = request.POST.get('product_quantity')

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
        
        # add product
        brand = Brand.objects.get(id = brand_id)
        category = Category.objects.get(id = catgory_id)
        product = Product(
            product_name = name,
            product_price = price,
            product_brand = brand,
            product_quantity = quantity,
            product_category = category,
            
        )
        product.save()

        for image in images:
            product_image = ProductImage(product=product, image = image)
            product_image.save()


        messages.success(request, ' successfully added')
 
    return redirect('product_list')


def search_product(request):
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


def delete_product(request,deleteproduct_id):
    dele = Product.objects.get(id = deleteproduct_id)
    dele.delete()
    return redirect('product_list')


def edit_product(request,editproduct_id):
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        brand_id = request.POST.get('product_brand')
        quantity = request.POST.get('product_quantity')

        #validatings the fields is empty
        if name.strip() == '':
            messages.error(request, 'Product name feilds is empty')
            return redirect('product_list')
        if price.strip() == '':
            messages.error(request, 'Product price is empty')
            return redirect('product_list')
        if brand_id.strip() == '':
            messages.error(request, 'shold take one brand')
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
        product.product_name = name
        product.product_price = price
        product.product_brand.brand_name = brand
        product.product_quantity = quantity
        product.save()
        messages.success(request, 'successfully edited')

    return render(request , 'category/category.html')


def product_view(request, viewproduct_id):
 
    # getings the products and returings the indivual product
    product = Product.objects.get(id = viewproduct_id)
    brand = Brand.objects.filter(is_available = True).order_by('id')
    category = Category.objects.filter(is_available = True).order_by('id')
    image_prodcut = ProductImage.objects.filter(product=product.id)
    print('images is the :',image_prodcut)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11')
    
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
    print('images is the :',product_image)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!11')
    if product:        
        context = {
            'product':product,
            'product_image':product_image
        }
        return render(request,'product/product_show.html',context)
    else:
        messages.error(request,'Not product found')
        return redirect('home:shop')
    

