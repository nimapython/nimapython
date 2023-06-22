from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from schoolapp.models import Person


# Create your views here.
def demo(request):
    obj=Person.objects.all()
    return render(request,'home.html',{'obj':obj})

def register(request):
    if request.method=='POST':
        uname=request.POST['username']
        password = request.POST['password']
        cpass = request.POST['cpass']
        if password==cpass:
            user=User.objects.create_user(username=uname,password=password)
            user.save()
            return redirect('login')

    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        uname=request.POST['username']
        password = request.POST['password']
        return redirect('form')
    return render(request,'login.html')

def form(request):
    if request.method=='POST':
        obj='Order Confirmed!!!!'
        return render(request,'order.html',{'obj':obj})
    return render(request,'form.html')
def order(request):
    return render(request,'order.html')
