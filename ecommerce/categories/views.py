from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Category , Brand
from django.contrib import messages , auth
from offer.models import Offer
# Create your views here.

@login_required(login_url='admin_login')
def categories(request):
    try:
        if request.user.is_superuser:
            categories = Category.objects.all()
            context = {
                'categories':categories
            }

            return render(request, 'category/category.html',context)
    except Exception as e:
        print(e)
        return render(request, 'category/category.html')


@login_required(login_url='admin_login')
def add_categories(request):
    try:
        if  request.user.is_superuser:
            if request.method == 'POST':
                name_categories = request.POST.get('name', None)           
                image_categories = request.FILES.get('image', None) 

                #validatings the fields is empty     
                if name_categories.strip() == '':
                    messages.error(request, ' name category field is empty!')
                    return redirect('add_categories')
                if Category.objects.filter(name=name_categories).exists():
                    messages.error(request,'the categories already taken!')
                    return redirect('add_categories')
                if not image_categories:
                    messages.error(request, 'images is not uploaded')
                    return redirect('add_categories')
                else:
                    new_category = Category(name=name_categories,image=image_categories)

                    
                    
                    new_category.save()
                    messages.success(request, 'Category added succesfully')
            categories = Category.objects.all()
            context = {
                'categories':categories
                }
                
        return render(request ,'category/category.html',context)
    except Exception as e:
        print(e)
        return render(request ,'category/category.html')
 


@login_required(login_url='admin_login')
def edit_categories(request,editcategory_id):
    try:
        if request.method == 'POST':
            name_categories = request.POST.get('name')
            image_categories = request.FILES.get('image')       
            img_category = Category.objects.get(id = editcategory_id)

            #validaitings the feilds is empty
            if image_categories:
                Category.image = image_categories
            else:
                messages.error(request,'image is not found')
                return redirect('add_categories')
            if name_categories.strip() == '':
                messages.error(request , ' the filed is empty')
                return redirect('add_categories')
            if Category.objects.filter(name = name_categories).exists():
                messages.error(request, 'category already taken')
                return redirect('add_categories')
                        
            # editings the category
            category = Category.objects.get(id=editcategory_id)
            category.categories =name_categories
            category.name = name_categories
            img_category.save()
            messages.success(request, 'succesfully edited')

        contegories = Category.objects.all()  
        context = {
            'categories': contegories
        }
        return render(request,'category/category.html',context)
    except Exception as e:
        print(e)
        return render(request ,'category/category.html')
    
@login_required(login_url='admin_login')
def search_categories(request):
    try:
        if request.method == 'POST':
            search = request.POST['search']

            #validatings the fields is empty
            if search is None or search.strip() == '':
                messages.error(request, 'fields is empty!')
                return redirect('search_categories')
            search_items = Category.objects.filter(name__icontains  = search, is_available =True )
            if search_items:    
                context = {
                    'search_items':search_items
                }
                return render(request,'category/category.html',context)
            else:
                messages.error(request, 'search not found')
                return redirect('search_categories')
        return render(request, 'category/category.html')
    except Exception as e:
        print(e)
        return render(request ,'category/category.html',context)

@login_required(login_url='admin_login')
def delete_categories(request,deletecategory_id):
    try:
        dele = Category.objects.get(id = deletecategory_id)
        dele.delete()
        return redirect('categories_list')
    except Exception as e:
        print(e)
        return render(request ,'category/category.html')

@login_required(login_url='admin_login')
def add_brand(request):
    try:
        if request.method == 'POST':
            name = request.POST['brand_name']
            image = request.FILES.get('brand_image')
            decs = request.POST['brand_discription']
            offer = request.POST.get('offer')

            #validatiings the fields is empty
            if name.strip() == '':
                messages.error(request, 'Brand name feild is empty!!')
                return redirect('add_brand')
            if decs.strip() == '':
                messages.error(request, 'Brand description is empty  ')
            if Brand.objects.filter(brand_name =name).exists():
                messages.error(request, ' Brand name is already exits!')
            if not image:
                messages.error(request, 'image is fields is empty!')
                return redirect('add_brand')
            
            # addings the brand
            new_brand = Brand(brand_name = name ,brand_image = image , brand_discription = decs , offer_id  = offer)
            new_brand.save()
            messages.success(request, 'Brand added successfully')
            return redirect('add_brand')
        brand = Brand.objects.all()
        offer = Offer.objects.all()
        context = {
            'brand':brand,
            'offer':offer
        }

        return render(request, 'category/brand.html',context)
    except Exception as e:
        print(e)
        return render(request, 'category/brand.html')


@login_required(login_url='admin_login')
def edit_brand(request ,editbrand_id ):
    try:
        if request.method == 'POST':
            name = request.POST.get('brand_name', None) 
            decs = request.POST.get('brand_discription',None)
            offer = request.POST.get('offer',None)

            #validatings image is empty or not and name is fields is empty
            try:
                image = request.FILES.get('brand_image', None)
                brand_item = Brand.objects.get(id = editbrand_id)
                if image:
                    brand_item.brand_image = image
                    brand_item.save()
            except Brand.DoesNotExist:
                messages.error(request, 'image is not found!')
            if name.strip == '':
                messages.error(request, 'the field is empty!')
                return redirect('add_brand')
            if Brand.objects.filter(brand_name = name).exists():
                check = Brand.objects.get(id = editbrand_id)
                if check == name:
                    pass
                else:
                    messages.error(request, 'name is already taken')
                    return redirect('add_brand')
                
            # Editings the Brand
            brand_item = Brand.objects.get(id = editbrand_id)
            if offer:
                offer_obj = Offer.objects.get(id = offer)
            else:
                offer_obj = None

            print('offer is the  ',offer)
            brand_item.brand_name = name
            brand_item.brand_discription = decs
            brand_item.offer = offer_obj
            brand_item.save()
            messages.success(request , 'succusfully edited')
            return redirect('add_brand')
        brand = Brand.objects.all()
        context  = {
            'brand':brand
        }

        return render(request, 'category/brand.html',context)
    except Exception as e:
        print(e)
        return render(request, 'category/brand.html')


@login_required(login_url='admin_login')
def search_brand(request):
    try:
        if request.method == 'POST':
            search = request.POST['search']

            #validatings the feilds is empty
            if search is None or search.strip() == '':
                messages.error(request, 'field is empty')
                return render(request , 'category/brand.html')
            brand = Brand.objects.filter(brand_name__icontains = search , is_available = True)
            if brand:
                context = {
                    'brand':brand
                }
                return render(request, 'category/brand.html', context)
            else:
                messages.error(request, 'search is not found')
                return render(request, 'category/brand.html')
    except Exception as e:
        print(e)
        return render(request, 'category/brand.html')
        
@login_required(login_url='admin_login')
def delete_brand(request,deletebrand_id):
    try:
        #deletings the brand items 
        dele = Brand.objects.get(id = deletebrand_id)
        dele.delete()
        return render(request, 'category/category.html')
    except Exception as e:
        print(e)
        return render(request, 'category/brand.html')

def adminpage(request):
    return redirect('adminside:dashboard')