from django.forms import ValidationError
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages , auth
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.models import User
from userauth.models import Customer
import re


def register_views(request):
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

                # validation field is empty
                if username.strip() == '' or email.strip() == '' or   password1.strip() == '' or password2.strip() == '' or gender.strip() == '': 
                    messages.info(request , ' field is empty!')
                    return render(request, 'user/register.html')
                elif Customer.objects.filter(username=username).exists():
                    messages.info(request, ' username is already taken')
                    return render(request, 'user/register.html')
                elif Customer.objects.filter(email = email).exists():
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

                # creating user
                new_user = Customer.objects.create_user(username=username , email= email , password=password1 , gender = gender)
                new_user.save()
                new_user.is_active=False
                new_user.last_login=None
                new_user.save()
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
    




def user_login(request):
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





def user_logout(request):
    auth.logout(request)
    return redirect('userauth:user_login')
   