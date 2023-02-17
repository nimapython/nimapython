from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def login(request):
    if request.method=='POST':
        uname=request.POST['login']
        pas=request.POST['p']
        user=auth.authenticate(username=uname,password=pas)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid username and password')
            return redirect('login')
    return render(request, 'login.html')
def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pas   = request.POST['pass']
        cpass = request.POST['cpass']
        if pas==cpass:
            if User.objects.filter(username=uname).exists():
                messages.info(request,'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=uname,password=pas,first_name=fname,last_name=lname,email=email)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/')
    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')