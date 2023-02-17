from xml.etree.ElementInclude import include


from django.urls import path

from demoapp import views

urlpatterns = [

    path('',views.demo,name='demo'),
    # path('',views.team,name='team'),

]