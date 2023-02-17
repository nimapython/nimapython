from django.shortcuts import render
from .models import place
from .models import team
# Create your views here.
def demo(request):
    obj=place.objects.all()
    obj2 = team.objects.all()
    return render(request,'index.html',{'result':obj,'m':obj2})



