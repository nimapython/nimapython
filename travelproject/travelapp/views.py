from django.shortcuts import render
from .models import Place
from .models import Team

from django.http import HttpResponse
# Create your views here.
def demo(request):
    obj=Place.objects.all()
    obj1 = Team.objects.all()
    return render(request,'index.html',{'result':obj,'result1':obj1})


# def about(request):
#     return render(request,'about.html')
#
# def addition(request):
#     x=int(request.GET['num1'])
#     y=int(request.GET['num2'])
#     res=x+y
#     return render(request,'result.html',{'result':res})