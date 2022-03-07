from django.shortcuts import render,redirect
from django.contrib import messages
import requests
from django.contrib.auth.models import User,auth
from .models import Userverification as userinfo
from difflib import SequenceMatcher
import string
import csv
import json
import smtplib,ssl
import random
csv.field_size_limit(100000000)
searches=False
def bubbleSort(arr,arr1,arr2):
    n = len(arr)
  
    for i in range(n-1):
        for j in range(0, n-1-i):
            if arr[j] < arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arr1[j],arr1[j+1]=arr1[j+1],arr1[j]
                arr2[j],arr2[j+1]=arr2[j+1],arr2[j]
    return arr1,arr2
def otp():
    return random.randint(1000,9999)
def send_email(email):
    port = 465  # For SSL
    password = "eesatvik.blend"
    context = ssl.create_default_context()
    o=otp()
    message=f"This is the otp {o}. Do not share with anyone!"
    print(message)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("nevzziffy@gmail.com", password)
        server.sendmail("nevzziffy@gmail.com", email, message)
    return o
def descending(keyword):
    k=[]
    c=[]
    title=[]
    keyword=" "+keyword.lower()
    for i in ['Australia','Brazil','China','France','Germany','India','Italy','Japan','Russia','Saudi Arabia','Singapore','South Africa',"United States","United Kingdom"]:
        with open("C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+i+'.csv','r',encoding="utf-8",errors="ignore") as file:
            file_reader=csv.reader(file)
            for line in file_reader:
                if line!=[]:
                    for j in range(len(line)):
                        if j%2==0:
                            if (line[j]).split("\n")[0] not in title:
                                title+=[(line[j]).split("\n")[0]]
                                k+=[line[j]]
                                if j+1!=len(line):
                                    c+=[line[j+1]]
                        
    COUNT=[]
    news1=[]
    h=[]
    
    for i in range(len(k)):
        if keyword in k[i].lower():
            count=(k[i].lower()).count(keyword)
        
            COUNT.append(count)
            news1.append(k[i])
            h.append(c[i])
    
    return bubbleSort(COUNT,news1,h)
def Trend(x):
    title=[]
    k=[]
    c=[]
    for i in x:
        for j in ['Australia','Brazil','China','France','Germany','India','Italy','Japan','Russia','Saudi Arabia','Singapore','South Africa',"United States","United Kingdom"]:
            with open("C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+j+'.csv','r',encoding="utf-8",errors="ignore") as file:
                file_reader=csv.reader(file)
                ctr=0
                for line in file_reader:
                    
                    if line!=[]:
                        if ctr==i:
                            for j in range(len(line)):
                                if j%2==0:
                                    if (line[j]).split("\n")[0] not in title:
                                        title+=[(line[j]).split("\n")[0]]
                                        k+=["\n".join((line[j].split("\n"))[1:])]
                                        if j+1!=len(line):
                                            c+=[line[j+1]]
                        ctr+=1
    return title,c,k
def image(x):
    c = []
    d = []
    with open(x,'r',encoding='utf-8') as file:
        csvr = csv.reader(file)
        for i in (csvr):
            if len(i) !=0:
                for r in range(len(i)):
                    if r%2==0:
                        if i[r].split("\n")[0]  not in d:
                        
                            j = i[r].split("\n")
                            v = j[0]
                            d +=[v]
                            if r+1!=len(i):
                                c+=[i[r+1]]
    return c,d
def art(x):
    c = []
    d = []
    e=[]
    
    with open(x,'r',encoding='utf-8') as file:
        csvr = csv.reader(file)
        for i in (csvr):
            if len(i) !=0:
                for r in range(len(i)):
                    if r%2==0:
                        if i[r].split("\n")[0] not in d:
                            j = i[r].split("\n")
                            v = j[0]
                            e+=["\n".join(j[1:])]
                            d +=[v]
                            if r+1!=len(i):
                                c+=[i[r+1]]
    return c,d,e
    
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
    elif SequenceMatcher(passwd.lower(),us.lower()).quick_ratio()>0.7:
        print("abc")
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
        
        new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\World.csv"
        c,d=image(new_path)
        c=json.dumps(c)
        d=json.dumps(d)
        return render(request,"home.html",{"Title":d,"Image":c})
    else:
        return redirect("/",permanent=True)
   

def sign_up(request):
    return render(request,'sign_up.html')

def genres(request):
    global USER
    global OTP
    global b
    try:
        m=int(request.POST["otp"])
    except:
        m=None
    if request.user.is_authenticated:
        b=True
    elif  m==OTP:
        username=USER["username"]
        password=USER["password"]
        email=USER["email"]
        
        user=User.objects.create_user(username=username,password=password,email=email)
        user.save()
        USER.pop("password")
        u=auth.authenticate(username=username,password=password)
        auth.login(request,u)
        
    else:
        messages.error(request,"Otp is incorrect")
        return redirect("/sign_up")
    return render(request,"genres.html")
def verify(request):
    global USER,b,OTP
    
    try:

        username=request.POST['username']
        password=request.POST['psw']
        email=request.POST['email']
        loc=request.POST['location']
    except:
        pass
    else:
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
 
    try:
        USER["username"]=username
        USER["location"]=loc
        USER["password"]=password
        USER["email"]=email
    except:
        pass
 
        
    OTP=send_email(USER['email'])
    print(OTP)
    
    return render(request,"verify.html")

def logout(request):
    auth.logout(request)
    return redirect('/',permanent=True)

def changepass(request):
    if request.method=="POST" and request.user.is_authenticated:
        current=request.POST["cpass"]
        new=request.POST["newpass"]
        user=User.objects.get(id=request.user.id)
        check=user.check_password(current)
        username=user.username
        print(username)
        if check:
            if password_check(new,username):
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
    global searches

    if request.user.is_authenticated:
        try:
            try:
                k=(request.GET["Noice"]) 
                try:
                    confirmation=request.GET["world"]
                    confirmation="World"
                except:
                    confirmation=request.GET["loc"]
                
                new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+confirmation+".csv"
                c,d,e=art(new_path)
                r=d[int(k)]
                c=c[int(k)]
                e=e[int(k)]
                e=e.replace("\n","<br>")
                r=json.dumps(r)
                c=json.dumps(c)
                e=json.dumps(e)
                return render(request,"article.html",{"Title":r,"Image":c,"Art":e})
            except:
                k=int(request.GET["Noice"])
                d=request.GET["keyword"]
                m,s=descending(d)
                s=s[k]
                content=m[k].split("\n")
                title=content[0]
                arti="\n".join(content[1:])
                
                
                searches=False
                arti=arti.replace("\n","<br>")
                return render(request,"article.html",{"Title":json.dumps(title),"Image":json.dumps(s),"Art":json.dumps(arti)})
        except:
            try:
                U=userinfo.objects.get(uname=request.user.username)
                j=U.genres
                p=j.split(" ")
                k=[]
                for i in p:
                    if i=="Sports":
                        k+=[0]
                    elif i=="Business":
                        k+=[1]
                    elif i=="Health":
                        k+=[2]
                    elif i=="Entertainment":
                        k+=[3]
                    elif i=="Science":
                        k+=[4]
                    elif i=="Technology":
                        k+=[5]
                d=request.GET["trending"]
                m=int(request.GET["Noice"])
                title,image,s=Trend(k)
                title=json.dumps(title[m])
                image=json.dumps(image[m])
                s=json.dumps(s[m])
                return render(request,"article.html",{"Title":title,"Image":image,"Art":s})
            except:
                U=userinfo.objects.get(uname=request.user.username)
                j=U.location
                k=int(request.GET["Noice"])
                new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+j+".csv"
                c,d,e=art(new_path)
                c=json.dumps(c[k])
                d=json.dumps(d[k])
                e=json.dumps(e[k])
                return render(request,"article.html",{"Title":d,"Image":c,"Art":e})   
                                    
        
    else:
        return redirect("/",permanent=True)
def search(request):
    global searches
    if request.user.is_authenticated:
        k=request.GET["keyword"]
        r,s=descending(k)
        j=[]
        
        
        for i in r:
            m=i.split("\n")
            
            j+=[m[0]]
            searches=True
        
        j=json.dumps(j)
        s=json.dumps(s)
        
        
        return render(request,"search.html",{"title":j,"image":s,"Key":k})
def trending(request):
    U=userinfo.objects.get(uname=request.user.username)
    j=U.genres
    p=j.split(" ")
    k=[]
    for i in p:
        if i=="Sports":
            k+=[0]
        elif i=="Business":
            k+=[1]
        elif i=="Health":
            k+=[2]
        elif i=="Entertainment":
            k+=[3]
        elif i=="Science":
            k+=[4]
        elif i=="Technology":
            k+=[5]
   
    title,image,s=Trend(k)
    title=json.dumps(title)
    image=json.dumps(image)
    return render(request,"trending.html",{"title":title,"image":image})
            
def nation(request):
    U=userinfo.objects.get(uname=request.user.username)
    j=U.location
    new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+j+".csv"
    c,d=image(new_path)
    c=json.dumps(c)
    d=json.dumps(d)
    return render(request,"nation.html",{"Title":d,"Image":c,"Loc":j})   
def countries(request):
    p=request.GET["loc"]
    new_path = "C:\\Users\\sathv\\ourwebsite\\Project\\getnews\\newscsv\\"+p+".csv"
    c,d=image(new_path)
    c=json.dumps(c)
    d=json.dumps(d)
    return render(request,"countries.html",{"title":d,"image":c,"Loc":p})

        
# Create your views here.
