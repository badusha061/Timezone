from django.shortcuts import render , redirect
from .models import Banner
from django.contrib import messages 
# Create your views here.


def banner(request):
    try:
        banner = Banner.objects.all()
        for i in banner:
            print(i.banner_image)
        context = {
            'banner':banner
        }
        return render(request,'adminside/banner.html',context)
    except Exception as e:
        print(e)
        return render(request,'adminside/banner.html')


def add_banner(request):
    try:
        if request.method == 'POST':
            banner_name = request.POST.get('banner_name')
            banner_image = request.FILES.get('banner_image')
            decs = request.POST.get('banner_discription')

            # validation 
            if banner_name.strip() =='' or decs.strip() == '':
                messages.error(request,'Field is Empty')
                return redirect('add_banner')
            if banner_image is None:
                messages.error(request,'The Image Fields is empty')
                return redirect('add_banner')
            if Banner.objects.filter(banner = banner_name).exists():
                messages.error(request,'name is already taken')
                return redirect('add_banner')
            
            banner = Banner()
            banner.banner = banner_name
            banner.banner_image = banner_image
            banner.caption = decs
            banner.save()
            messages.success(request,'Successfully Added into Banner')
            return redirect('banner')
        return redirect('banner')
    except Exception as e:
        print(e)
        return redirect('banner')

def edit_banner(request,editbanner_id):
    try:
        if request.method == 'POST':
            banner_name = request.POST.get('banner_name')
            banner_dec = request.POST.get('banner_discription')
            
            #validation
            if banner_name.strip() == '' or banner_dec.strip() == '':
                messages.error(request,'Filed is empty')
                return redirect('banner')
            if Banner.objects.filter(banner = banner_name).exists():
                messages.error(request,'name is already taken')
                return redirect('banner')
            
            banner = Banner.objects.get(id = editbanner_id)
            
            banner_image = request.FILES.get('image')
            if banner_image:
                banner.banner_image = banner_image
            else:
                messages.error(request, 'The Image Field is empty')
                return redirect('banner')
            
            banner.banner = banner_name
            banner.caption =banner_dec
            banner.save()
            messages.success(request,'Successfully edited Brand')
            return redirect('banner')
        
        return render(request,'adminside/banner.html')
    except Exception as e:
        print(e)
        return render(request, 'adminside/banner.html')


def delete_banner(request,deletebanner_id):
    try:
        banner = Banner.objects.get(id = deletebanner_id)
        banner.delete()
        messages.success(request,'Successfully Deleted')
        return redirect('banner')
    except Exception as e:
        print(e)
        return redirect('banner')