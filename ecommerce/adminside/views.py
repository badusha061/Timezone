from django.shortcuts import render , redirect
from django.contrib import messages , auth
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views import View
# Create your views here.


@login_required(login_url = 'adminside:admin_login')
def dashboard(request):
    
    if request.user.is_superuser:
       
        user = User.objects.all()
        context = {
            'user':user
        }
        return render(request,'adminside/dashboard.html',context)
    else:       
        return redirect( 'adminside:admin_login')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username = username , password = password)

        #validatings the fiels is empty
        if username.strip() == '' or password == '':
            messages.error(request , 'fields empty !!!')
            return redirect('adminside:admin_login')
        
        if user and user.is_superuser:
            login(request , user)
            return redirect('adminside:dashboard')
        else:
            messages.error(request ,'Invalid credentials. Please try again.')
            return redirect('adminside:admin_login')
    return render(request, 'adminside/admin_login.html')


@login_required(login_url = 'adminside:admin_login')
def user_mgt(request):
    users = User.objects.all().order_by('id')
    context = {
        'users': users
    }

    return render(request, 'adminside/usermgt.html', context)


@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('adminside:admin_login')


@login_required(login_url='admin_login')
def user_block(request,user_id):
    

    # user is block 
    user = User.objects.get(id = user_id)
    if user.is_active:  
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('adminside:user_mgt')


@login_required(login_url='admin_login')
def user_search(request):
    search = request.POST.get('search')

    # validatings the search is empty
    if search is None or  search.strip() == '':
        messages.error(request , 'field is empty')
        return redirect('adminside:user_mgt')
    users = User.objects.filter(Q(username__icontains = search)| Q(email__icontains = search))
    context = {
        'users':users
    }
    if users:
        pass
    else:
        users : False
        messages.error(request , 'Search is not found')
        return redirect('adminside:user_mgt')
    return render(request, 'adminside/usermgt.html',context)


@login_required(login_url = 'adminside:admin_login')
def user_block_status(request):
    name = request.POST.get('name')
    if name == 'Active':
        users = User.objects.filter(is_active = True)
        context = {
            'users':users
        }
        return render(request , 'adminside/usermgt.html',context)
    if name == 'Blocked':
        users = User.objects.filter(is_active = False)
        context = {
            'users':users
        }
        return render(request ,'adminside/usermgt.html',context)
    if name == 'All':
        users = User.objects.all()
        context = {
            'users':users
        }
        return render(request, 'adminside/usermgt.html',context)


def adminpage(request):
    return redirect('adminside:dashboard')