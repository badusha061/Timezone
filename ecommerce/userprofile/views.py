from django.shortcuts import render , redirect
from .import views
from django.core.exceptions import ObjectDoesNotExist
from .models import Address
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
# Create your views here.

def userprofile(request):

    
    context = {
        'address': Address.objects.filter(user=request.user,is_available=True),
        
    }
    print(context,'----------------------------------------------------')
    return render(request , 'user/userprofile.html' , context)


def add_address(request):
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
            return redirect('userprofile')

        if firstname.strip() == '':
            messages.error(request , 'First name fiels is empty')
            return redirect('userprofile')
        if lastname.strip() == '':  
            messages.error(request ,'Last name is empty')
            return redirect('userprofile')
        if number.strip() == '':
            messages.error(request, 'Number feilds is empty')
            return redirect('userprofile')
        if email.strip() == '':
            messages.error(request, 'Email feild is empty')
            return redirect('userprofile')
        if address_user.strip() == '':
            messages.error(request , 'Address feilds is empty')
            return redirect('userprofile')
        if country.strip() == '':
            messages.error(request, 'Country feild is empty')
            return redirect('userprofile')
        if state.strip() == '':
            messages.error(request , 'State feild is empty')
            return redirect('userprofile')
        if city.strip() == '':
            messages.error(request, 'City feilds is empty')
            return redirect('userprofile')
        if pincode.strip() == '':
            messages.error(request , 'Pincode is empty')
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
        print(address_item)
        address_item.save()
        messages.success(request, 'Succesffully added')
        return redirect('userprofile')
    return redirect('userprofile')

   

def edit_address(request,editaddress_id):
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
            return redirect('userprofile')

        if firstname.strip() == '':
            messages.error(request , 'First name fiels is empty')
            return redirect('userprofile')
        if lastname.strip() == '':  
            messages.error(request ,'Last name is empty')
            return redirect('userprofile')
        if number.strip() == '':
            messages.error(request, 'Number feilds is empty')
            return redirect('userprofile')
        if email.strip() == '':
            messages.error(request, 'Email feild is empty')
            return redirect('userprofile')
        if address.strip() == '':
            messages.error(request , 'Address feilds is empty')
            return redirect('userprofile')
        if country.strip() == '':
            messages.error(request, 'Country feild is empty')
            return redirect('userprofile')
        if state.strip() == '':
            messages.error(request , 'State feild is empty')
            return redirect('userprofile')
        if city.strip() == '':
            messages.error(request, 'City feilds is empty')
            return redirect('userprofile')
        if pincode.strip() == '':
            messages.error(request , 'Pincode is empty')
            return redirect('userprofile')


        #Editings the address
        address = Address.objects.get(id = editaddress_id)

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
        return redirect('userprofile')
    else:
        return redirect('userprofile')




def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST['email']

        # validatings the fields is empty
        if username.strip() == '':
            messages.error(request , 'Username feilds is empty')
            return redirect('userprofile')
        if email.strip() == '':
            messages.error(request , 'Email fields is empty')
            return redirect('userprofile')
        try:

            #Editings the updated
            user = User.objects.get(username = request.user)
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'UserProfile Updated Successfully')
        except ObjectDoesNotExist:
            messages.error(request , 'User does not exist')
    return redirect('userprofile')
        

def changepassword(request):
    if request.method == 'POST':
        oldpssword = request.POST['old_password']
        newpassword = request.POST['new_password']
        conforpassword = request.POST['confirm_new_password']

        #validatings the password
        if newpassword != conforpassword:
            messages.error(request , 'Password do not match please enter correct')
            return redirect('userprofile')
        user = User.objects.get(username = request.user)
        if oldpssword.strip() == '' or newpassword.strip() == '' or conforpassword.strip() == '':
            messages.error(request , 'Feilds is empty')
            return redirect('userprofile')
        
        # if check the password
        if check_password(oldpssword , user.password):
            user.set_password(newpassword)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Successfully updated password')
            return redirect('userprofile')
        else:
            messages.error(request , 'Old password do not match')
            return redirect('userprofile')

    return redirect('userprofile')

def delete_address(request,deleteaddress_id):
    if request.method == 'POST':
        dele = Address.objects.get(id =deleteaddress_id )
        dele.is_available = False
        dele.save()
        return redirect('userprofile')
    else:
        return redirect('userprofile')
    
def edit_image(request):
    if request.method == 'POST':
        image = request.FILES.get('user_image')
        
        #validatings the field is empty
        if image.strip() == '':
            messages.error(request  ,'Image fields is empty')
            return redirect('userprofile')
        address = Address.objects.filter(user = request.user).first()
        if address:       
            address.image = image
            address.save()
            messages.success(request , 'Successfully updated Image')
            return redirect('userprofile')
        else:
            messages.error(request, 'Image is not found')
    else:
        return redirect('userprofile')