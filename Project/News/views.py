from django.shortcuts import render,redirect
from django.contrib import messages
import requests
from django.contrib.auth.models import User,auth
from .models import Userverification as userinfo

import string
USER=[]
def password_check(passwd):
    SpecialSym =string.punctuation
    val = True
      
    if len(passwd) < 6:
        print('length should be at least 6')
        val = False
          
    if len(passwd) > 20:
        print('length should be not be greater than 8')
        val = False
          
    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False
          
    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False
          
    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False
          
    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    
    return val
  

def emailverifier(email):
    response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': email})

    status = response.json()['status']
    if status=="valid":
        return True
    else:
        return False
def response(request):
    return render(request,'login.html')
def login(request):
    global USER
    try:
        username=request.POST['uname']
        password=request.POST['psw']
        user= auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            return render(request,"home.html")
        elif not User.objects.filter(username=username).exists():
            messages.error(request,"Username does not exist")
            return redirect("/")
        else:
            messages.error(request,"Password is incorrect")
            return redirect("/")
    except:
        try:
            d={}
            L=['Sports','Business','Health','Entertainment','Science','Technology','Nation']
            for i in L:
                try:
                    request.POST[i]
                    d[i]=True
                except:
                    d[i]=False
            genres=""
            for i in d:
                if d[i]:
                    genres+=i+" "
            USER+=[genres]
            k=userinfo(uname=USER[0],location=USER[1],genres=USER[2])  
            k.save()  
        except:
            pass
        return render(request,"home.html")

def sign_up(request):
    return render(request,'sign_up.html')
def genres(request):
    global USER
    try:
        username=request.POST['username']
        password=request.POST['psw']
        confirm=request.POST['pswr']
        email=request.POST['email']
        loc=request.POST['location']
       
        if password!=confirm:
            messages.error(request,'Password does not match confirm')
            return redirect('/sign_up')
        if not password_check(password):
            messages.error(request,"Enter a stronger password")
            return redirect('/sign_up')
        elif emailverifier(email)==False:
            messages.error(request,email+" does not exist")
            return redirect('/sign_up')
        elif User.objects.filter(username=username).exists():
            messages.error(request,"Username already taken")
            return redirect('/sign_up')
        elif User.objects.filter(email=email).exists():
            messages.error(request,"Email already taken")
            return redirect('/sign_up')
        
        else:
            user=User.objects.create_user(username=username,password=password,email=email)
            USER=[username,loc]
            user.save()
    
    except:
        pass
    return render(request,'genres.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
def changepass(request):
    if request.method=="POST":
        current=request.POST["cpass"]
        new=request.POST["newpass"]
        confirm=request.POST["confnewpass"]
        if new!=confirm:
            messages.error(request,"Confirm and Password not matching")
            return redirect("/changepass")
        user=User.objects.get(id=request.user.id)
        check=user.check_password(current)
        if check:
            if password_check(new):
                user.set_password(new)
                user.save()
                messages.success(request,"Succesfully changed the password")
                return redirect("/home")
            else:
                messages.error(request,"Password conditions not met")
                return redirect("/changepass")
        else:
            messages.error(request,"Wrong password")
            return redirect("/changepass")


    return render(request,"changepass.html")

# Create your views here.
