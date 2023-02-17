#
#
# from .models import Task
# from django import forms
# class TodoForm(forms.ModelForm):
#     class meta:
#         model = Task
#         fields = ['name', 'priority', 'date']
from .models import Task
from django import forms
class Todoform(forms.ModelForm):
    class Meta:
        model=Task
        fields=['name','priority','date']






