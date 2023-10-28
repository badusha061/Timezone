from django.shortcuts import render , redirect
from .import views
from django.core.exceptions import ObjectDoesNotExist
from .models import Address , Wallet , Transaction
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from userauth.models import Customer
import re
from django.core.validators import validate_email
from django.forms import ValidationError
# Create your views here.

def userprofile(request):
    try:
        wallet = 0
        try:
            wallet = Wallet.objects.filter(user = request.user).first()

        except Wallet.DoesNotExist:
            wallet = 0
        
        try:
            user = Customer.objects.get(id = request.user.id)
        except Customer.DoesNotExist:
            user = None
        user_auth = User.objects.get(id = request.user.id)


        context = {
            'address': Address.objects.filter(user=request.user,is_available=True),
            'wallet':wallet,
            'user':user,
            'user_auth':user_auth
            
            }
        return render(request , 'user/userprofile.html' , context)
    except Exception as e:
        print(e)
        return render(request, 'user/userprofile.html')


def add_address(request):
    try:
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
            if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),number):
                messages.error(request,'Enter valid phone number')
                return redirect('userprofile')
            phonenumber_checkings = len(number)
            if not phonenumber_checkings == 10:
                messages.error(request, 'Phone Number should be 10 digits')
                return redirect('userprofile')
            
            if email.strip() == '':
                messages.error(request, 'Email feild is empty')
                return redirect('userprofile')
            
            email_check = validator_email(email)
            if email_check is False:
                messages.error(request, 'Email is not valid')
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
            if not re.search(re.compile(r'^\d{6}$'),pincode):
                messages.error(request,'Should only 6 contain numeric')
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
            address_item.save()
            messages.success(request, 'Succesffully added')
            return redirect('userprofile')
        return redirect('userprofile')
    except Exception as e:
        print(e)
        return redirect('userprofile')

   

def edit_address(request,editaddress_id):
    try:
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
            if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),number):
                messages.error(request,'Enter valid phone number')
                return redirect('userprofile')
            phonenumber_checkings = len(number)
            if not phonenumber_checkings == 10:
                messages.error(request, 'Phone Number should be 10 digits')
                return redirect('userprofile')
            
            if email.strip() == '':
                messages.error(request, 'Email feild is empty')
                return redirect('userprofile')
                    
            email_check = validator_email(email)
            if email_check is False:
                messages.error(request, 'Email is not valid')
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
            
            if not re.search(re.compile(r'^\d{6}$'),pincode):
                messages.error(request,'Should only 6 contain numeric')
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
    except Exception as e:
        print(e)
        return redirect('userprofile')




def edit_profile(request):
    try:
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
    except Exception as e:
        print(e)
        return redirect('userprofile')
        

def changepassword(request):
    try:
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
    except Exception as e:
        print(e)
        return redirect('userprofile')

def delete_address(request,deleteaddress_id):
    try:
        if request.method == 'POST':
            dele = Address.objects.get(id =deleteaddress_id )
            dele.is_available = False
            dele.save()
            return redirect('userprofile')
        else:
            return redirect('userprofile')
    except Exception as e:
        print(e)
        return redirect('userprofile')
    
def edit_image(request):
    try:
        if request.method == 'POST':
            images = request.FILES.get('user_image')

            #validatings the field is empty
            if images is None:
                messages.error(request  ,'Image fields is empty')
                return redirect('userprofile')
            
            image = User.objects.get(id = request.user.id)
            print('the images is the ',image)
            if image:
                cus = Customer.objects.get(username = image)
                cus.images = images
                cus.save()
                messages.success(request,'Successfully Changed')
                return redirect('userprofile')
        else:
            return redirect('userprofile')
    except Exception as e:
        print(e)
        return redirect('userprofile')
    


def wallet(request):
    try:
        wallet = Wallet.objects.filter(user = request.user).first()
        tra = Transaction.objects.filter(wallet = wallet)
        
        try:
            user = Customer.objects.get(id = request.user.id)
        except Customer.DoesNotExist:
            user = None
        context = {
            'wallet':wallet,
            'tra':tra,
            'user_auth':user
        }
        return render(request,'user/wallet.html',context)
    except Exception as e:
        print(e)
        return render(request, 'user/wallet.html')




def validator_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
    

def chat_box(request):
    return render(request, 'user/chat.html')