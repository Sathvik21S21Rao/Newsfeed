from django.shortcuts import render,redirect
from django.contrib import messages
import requests
from django.contrib.auth.models import User,auth
from .models import Userverification as userinfo
USER=''
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

# Create your views here.
