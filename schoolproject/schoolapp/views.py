from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def demo(request):
    return render(request,'home.html')

def register(request):
    if request.method=='POST':
        uname=request.POST['username']
        password = request.POST['password']
        cpass = request.POST['cpass']
        user=User.objects.create_user(username=uname,password=password)
        user.save()
        return redirect('login')
    else:
        return render(request,'register.html')

def login(request):
    if request.method=='POST':
        uname=request.POST['username']
        password = request.POST['password']
        return redirect('form')
    return render(request,'login.html')

def form(request):
    return render(request,'form.html')
