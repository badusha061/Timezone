from django.forms import ValidationError
from django.shortcuts import render , redirect 
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages , auth
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User
from userauth.models import Customer , Profile
import re
from .helpers import send_forget_password_mail
import uuid
import string
from userprofile.models import Wallet
from functools import wraps



def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('userprofile')  # or wherever you want logged-in users to go
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@anonymous_required
def register_views(request):
    try:
        if request.user.is_authenticated:
            return redirect('userprofile')

        if request.method == 'POST': 
            
            #otp with signup
            get_otp=request.POST.get('otp')
            if get_otp:
                get_email=request.POST.get('email')
                user=Customer.objects.get(email=get_email)
                if not re.search(re.compile(r'^\d{6}$'), get_otp): 
                    messages.error(request,'OTP should only contain numeric!')
                    return render(request,'user/register.html',{'otp':True,'user':user})  

                session_otp=request.session.get('otp')
                if int(get_otp) == session_otp:
                    user.is_active=True
                    user.save()
                    auth.login(request,user)
                    messages.success(request,f'Account is created for {user.username}')
                    
                    return redirect('userauth:user_login')
                else:
                    messages.warning(request,f'you Entered a Wrong OTP')
                    return render(request,'user/register.html',{'otp':True,'user':user})
            else:
                get_otp=request.POST.get('otp1')
                email=request.POST.get('user1')
                if get_otp:
                    user=Customer.objects.get(email=email)
                    messages.error(request,'field cannot empty!')
                    return render(request,'user/register.html',{'otp':True,'user':user})
                else:
                                            
                    username = request.POST['username'] 
                    email = request.POST['email']
                    gender = request.POST['gender']
                    password1 = request.POST['password1']
                    password2 = request.POST['password2']
                    refferal_code = request.POST.get('referal_offer')
                    
                        
                    #validation field is empty
                    if username.strip() == '' or email.strip() == '' or   password1.strip() == '' or password2.strip() == '' or gender.strip() == '': 
                        messages.info(request , ' field is empty!')
                        return render(request, 'user/register.html')
                    elif Customer.objects.filter(username=username).exists():
                        user1 = Customer.objects.get(username = username)
                        if user1.last_login is None:
                            user1.delete()
                        else:
                            messages.info(request, ' username is already taken')
                            return render(request, 'user/register.html')
                    elif Customer.objects.filter(email = email).exists():
                            user = Customer.objects.get(email = email)
                            if user.last_login is None:
                                user.delete()
                            else:
                                messages.info(request, ' email is already taken')
                                return render(request, 'user/register.html')

                    elif password1 != password2:
                        messages.info(request,'password do not match')
                        return render(request, 'user/register.html')
                    email_check = validator_email(email)
                    if email_check is False:
                        messages.info(request, 'email is not valid ')
                        return render(request, 'user/register.html')
                    password_check = validator_password(password1)
                    if password_check is False:
                        messages.info(request, 'Please enter a strong password!')
                        return render(request, 'user/register.html')
                    

                    if refferal_code:
                        try:
                            referrer = Customer.objects.get(refferal_code=refferal_code)
                            print('the refferal code is the',refferal_code)
                            print(referrer.username)
                            wallet, created = Wallet.objects.get_or_create(user=referrer)
                            if created:
                                wallet.wallet = 0
                                wallet.user = referrer    # Initialize the wallet amount if it's a new wallet.
                            wallet.wallet += 100
                            wallet.save()
                            print('saved the to the wallet')
                        except Customer.DoesNotExist:
                            referrer = None
                    else:
                        referrer = None

                    print(referrer)
                    # creating user
                    new_user = Customer.objects.create_user(username=username , email= email , password=password1 , gender = gender)
                    new_user.refferal_code   = generate_referral_code()
                    new_user.referrer = referrer
                    new_user.save()
                    new_user.is_active=False
                    new_user.last_login=None
                    new_user.save()

                    refferish = Customer.objects.get(email=email)
                    if refferish.referrer:
                        wallet = Wallet.objects.get(user = refferish.referrer)
                        wallet.wallet += 100 
                        wallet.save()

                    user_otp=random.randint(100000,999999)
                    request.session['otp']=user_otp
                    mess=f'Hello \t{new_user.username},\nYour OTP to verify your account for time zone  is {user_otp}\n Thanks You!'
                    send_mail(
                            "Welcome to Time Zone , verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [new_user.email],

                            fail_silently=False
                        )
                    return render(request,'user/register.html',{'otp':True,'user':new_user})         

        return render(request,  'user/register.html')
    except Exception as e:
        print(e)
        return render(request, 'user/register.html')


#validate email
def validator_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    
#validate password
def validator_password(password1):
    try:
        validate_password(password1)
        return True
    except ValidationError:
         return False    
    
# generate refferal code 
def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))






@anonymous_required
def user_login(request):
    try:    
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            #validate fields is empty
            if username.strip() == '' or password.strip() == '':
                messages.error(request, 'Field is empty')
                return redirect('userauth:user_login')

            user = authenticate(username=username, password=password)

            if user is not None:
                    if user.is_active:

                        login(request, user)
                        return redirect('home:home')
                    else:
                        messages.warning(request,'your account has been blocked!')
                        redirect('userauth:user_login')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('userauth:user_login')

        return render(request, 'user/login.html')
    except Exception as e:
        print(e)
        return render(request, 'user/login.html')





def user_logout(request):
    auth.logout(request)
    return redirect('userauth:user_login')
   

def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if username.strip() == '':
                messages.success(request,'Username field is empty')
                return redirect('userauth:forget_password')
            if User.objects.filter(username = username).exists():
                user_obj = User.objects.get(username = username)
                print('the user object is the',user_obj)
                token = str(uuid.uuid4())
                try:
                        
                    profile_obj = Profile.objects.get(user = user_obj )
                    profile_obj.forget_password_token = token   
                    profile_obj.save()
                    print('the try work')
                except Profile.DoesNotExist:
                    profile_obj = Profile(user = user_obj,forget_password_token = token)
                    profile_obj.save()
                    print('the except work')
                send_forget_password_mail(user_obj.email,token)
                messages.success(request,'Email is sent.')
                return redirect('userauth:forget_password')
            else:
                messages.error(request,'User Not Found')
                return redirect('userauth:forget_password')
        return render(request,'user/forget.html')
    except Exception as e:
        print(e)
        return render(request,'user/forget.html')



def change_password(request,token):
    try:
        context = {}
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        if request.method == 'POST':
            password1 = request.POST.get('password')
            password2 = request.POST.get('password1')
            user_id = request.POST.get('user_id')
            if user_id is None:
                messages.error(request,'User Not Found')
                url_path = reverse('userauth:change_password', kwargs={'token': token})
                return redirect(url_path)
            if password1 != password2:
                messages.error(request,'Password Do Not Match')
                url_path = reverse('userauth:change_password', kwargs={'token': token})
                return redirect(url_path)
            if password1.strip() == '' or password2.strip() == '':
                messages.error(request, 'Filed is empty')
                url_path = reverse('userauth:change_password', kwargs={'token': token})
                return redirect(url_path)
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(password1)
            user_obj.save()
            messages.success(request,'Successfully Changed Passwdord')
            return redirect('userauth:user_login')
        print(profile_obj)
        context = {
            'user_id':profile_obj.user.id
        }
        return render(request,'user/change.html',context)
    except Exception as e:
        print(e)
        return render(request, 'user/change.html')
