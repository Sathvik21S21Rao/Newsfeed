from django.shortcuts import render
def response(request):
    return render(request,'login.html')
def sign_up(request):
    return render(request,'sign_up.html')
def genres(request):
    return render(request,'genres.html')
# Create your views here.
