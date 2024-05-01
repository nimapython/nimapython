from django import forms
from .models import Cars,User

class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['brand', 'name', 'mileage', 'price', 'location', 'description', 
                  'registration_year', 'registration_number', 'engine_capacity', 
                  'insurance', 'spare_key', 'transmission', 'fuel_type', 'img']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','name','email','phone_number']