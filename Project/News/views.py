from django.shortcuts import render,redirect
from django.contrib import messages
def response(request):
    return render(request,'login.html')
def sign_up(request):
    
    return render(request,'sign_up.html')
def genres(request):
    try:
        username=request.POST['username']
        password=request.POST['psw']
        confirm=request.POST['pswr']
        loc=request.POST['location']
        if password!=confirm:
            messages.info(request,'Password does not match confirm')
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
        messages.info(request,'Choose atleast one genre')
        return redirect('/genres')
    
   

    return render(request,'home.html')

# Create your views here.
