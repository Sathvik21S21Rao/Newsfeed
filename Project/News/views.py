from django.shortcuts import render,redirect
from django.contrib import messages
import requests
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
def sign_up(request):
    
    return render(request,'sign_up.html')
def genres(request):
    try:
        username=request.POST['username']
        password=request.POST['psw']
        confirm=request.POST['pswr']
        email=request.POST['email']
        loc=request.POST['location']
        if password!=confirm:
            messages.error(request,'Password does not match confirm')
            return redirect('/sign_up')
        if emailverifier(email)==False:
            messages.error(request,email+" does not exist")
            return redirect('/sign_up')
        

    except:
        pass
 

    return render(request,'genres.html')
def home(request):
    d={}
    L=['Sports','Business','Health','Entertainment','Science','Technology','Nation']
    for i in L:
        try:
            request.POST[i]
            d[i]=True
        except:
            d[i]=False
    
    print(d)
    for i in d:
        if d[i]:
            break
    else:
        return redirect('/genres')
    
   

    return render(request,'home.html')

# Create your views here.
