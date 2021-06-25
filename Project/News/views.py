from django.shortcuts import render,redirect
from django.contrib import messages
import requests
from django.contrib.auth.models import User,auth
from .models import Userverification as userinfo
import sys
from difflib import SequenceMatcher
import string
import csv
import json
def image(x):
    c = []
    d = []
    with open(x,'r',encoding='utf-8') as file:
        csvr = csv.reader(file)
        for i in (csvr):
            if len(i) !=0:
                for r in range(len(i)):
                    if r%2 !=0:
                        c += [i[r]]
                    else:
                        j = i[r].split("\n")
                        v = j[0]
                        d +=[v]
    return c,d
def art(x):
    c = []
    d = []
    with open(x,'r',encoding='utf-8') as file:
        csvr = csv.reader(file)
        for i in (csvr):
            if len(i) !=0:
                for r in range(len(i)):
                    if r%2 !=0:
                        c += [i[r]]
                    else:
                        j = i[r]
                        v = j
                        d +=[v]
    return c,d
    
USER={"username":"","location":"","genres":""}
b=False
b1=False
def password_check(passwd,us):
    SpecialSym =string.punctuation
    
      
    if len(passwd) < 8:
        print('length should be at least 8')
        return False
          
    elif len(passwd) > 20:
        print('length should be not be greater than 20')
        return False
          
    elif not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        return False
          
    elif not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        return False
          
    elif not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        return False
          
    elif not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        return False
    elif SequenceMatcher(passwd.lower(),us.lower()).quick_ratio()>0.5:
        return False
    
    return True
  

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
    if request.user.is_authenticated:
        auth.logout(request)
    return render(request,'login.html')

def login(request):
    global USER,b,b1


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
                    request.GET[i]
                    d[i]=True
                except:
                    d[i]=False
            genres=""
            for i in d:
                if d[i]:
                    genres+=i+" "

            
            if USER["username"]!="":
                USER['genres']=genres
                k=userinfo(uname=USER["username"],location=USER["location"],genres=USER["genres"])
                k.save()  
            USER={"username":"","location":"","genres":""}
            
            
        except:
            pass

    if request.user.is_authenticated:
        if b:
            U=userinfo.objects.get(uname=request.user.username)
            k=U.genres
            d={}
            L=['Sports','Business','Health','Entertainment','Science','Technology','Nation']
            for i in L:
                try:
                    request.GET[i]
                    d[i]=True
                except:
                    d[i]=False
            genres=""
            for i in d:
                if d[i]:
                    genres+=i+" " 
            if k!="" and genres=="":
                genres=k  
            U.genres=genres
            U.save()
            b=False
            return redirect("/home",permanent=True)
 

    if request.user.is_authenticated:
        
        new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\World.csv"
        c,d=image(new_path)
        c=json.dumps(c)
        d=json.dumps(d)
        return render(request,"home.html",{"Title":d,"Image":c})
    else:
        return redirect("/",permanent=True)
   

def sign_up(request):
    return render(request,'sign_up.html')

def genres(request):
    global USER,b
    try:
        

        username=request.POST['username']
        password=request.POST['psw']
        email=request.POST['email']
        loc=request.POST['location']
        
        if not password_check(password,username):
            
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
 
        
        
       
        user=User.objects.create_user(username=username,password=password,email=email)
        user.save()
        USER["username"]=username
        USER["location"]=loc
            
        u=auth.authenticate(username=username,password=password)
        if u:
            print("abc")
            auth.login(request,u)
        else:
            print("def")
    
    except:
        print(sys.exc_info)
        b=True
    
    
    return render(request,"genres.html")


def logout(request):
    auth.logout(request)
    return redirect('/',permanent=True)

def changepass(request):
    if request.method=="POST" and request.user.is_authenticated:
        current=request.POST["cpass"]
        new=request.POST["newpass"]
        user=User.objects.get(id=request.user.id)
        check=user.check_password(current)
        if check:
            if password_check(new):
                user.set_password(new)
                user.save()
                messages.success(request,"Password successfully changes.")
                return redirect("/home",permanent=True)
                
            else:
                messages.error(request,"Password conditions not met")
                return redirect("/changepass")
        else:
            messages.error(request,"Wrong password")
            return redirect("/changepass")
        
    if request.user.is_authenticated:
        return render(request,"changepass.html")
    else:
        return redirect("/",permanent=True)
def location(request):

    
    if request.user.is_authenticated and request.method=="POST":
    
                   
        
        U=userinfo.objects.get(uname=request.user.username)
        k=U.location
        print(k)
        locations=['Australia','Brazil','China','France','Germany','India','Italy','Japan','Russia','Saudi_Arabia','Singapore','South_Africa','United_Kingdom','United_States']
        locs=""
        for i in locations:
    
            if (request.POST.get(i)):
    
                locs=i
                break
            
        print(locs)
        if k!="" and locs=="":
            locs=k
        if "_" in locs:
            locs=locs.replace("_"," ")
        U.location=locs
            
        U.save()       

        return redirect("/home",permanent=True)
    if request.user.is_authenticated:
        
        return render(request,"location.html")
    else:
        return redirect("/",permanent=True)
def articles(request):
    if request.user.is_authenticated:
        k=(request.GET["Noice"])
        new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\World.csv"
        c,d=art(new_path)
        c=json.dumps(c)
        r=d[int(k)]
        print(r)
        r=json.dumps(r)
        return render(request,"article.html",{"Art":r,"Image":c})
    
    else:
        return redirect("/",permanent=True)
            
            

# Create your views here.
