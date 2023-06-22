
from django.contrib import admin
from django.urls import path, include
from schoolapp import views
from .views import register,login,form

urlpatterns = [
    path('',views.demo,name='demo'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('form',views.form,name='form'),
    # path('order', views.order, name='order'),

]
