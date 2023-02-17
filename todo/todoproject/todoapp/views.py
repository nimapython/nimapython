from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .models import Task
from .forms import Todoform
from django .views.generic import ListView
from django .views.generic.detail import DetailView
from django .views.generic.edit import UpdateView,DeleteView
# Create your views here.
class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task'

class Taskdetailview(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class Taskupdateview(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url= reverse_lazy('cbvhome')


def add(request):
    task = Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('task')
        priority = request.POST.get('priority')
        date = request.POST.get('date')
        task=Task(name=name,priority=priority,date=date)
        task.save()
        return redirect('/')
    return render(request,'home.html',{'task':task})

# def detail(reqyest):
#     task=Task.objects.all()
#     return render(reqyest,'detail.html',{'task':task})

def delete(request,id):
    if request.method=='POST':
        task = Task.objects.get(id=id)
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

# def edit(request,id):
#     task = Task.objects.get(id=id)
#     form = TodoForm(request.POST or None, instance=task)
#     if form.is_valid():
#         form.save()
#         return redirect('/')
#     return render(request,'edit.html',{'form':form,'task':task})

def update(request,id):
    task=Task.objects.get(id=id)
    form=Todoform(request.POST or None,instance=task)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'edit.html',{'form':form,'task':task})
