from django.conf import settings
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),

    path('register/',views.register,name='register'),
    path('slogin/',views.slogin,name='slogin'),
    path('sregister/',views.sregister,name='sregister'),
    path('sindex/',views.sindex,name='sindex'),
    path('addcar/',views.addcar,name='addcar'),
    path('home/',views.home,name='home'),
    path('car_detail/<int:car_id>/',views.car_detail,name='car_detail'),
     path('mycar_detail/<int:car_id>/',views.mycar_detail,name='mycar_detail'),
    path('slogout/',views.slogout,name='slogout'),
    path('logout/',views.logout,name='logout'),
    path('buy_now/<int:car_id>/',views.buy_now,name='buy_now'),
    path('aindex/',views.aindex,name='aindex'),
    path('sellerbookings/',views.sellerbookings,name='sellerbookings'),
    path('bookings/',views.bookings,name='bookings'),
    path('cancel_booking/<int:booking_id>/',views.cancel_booking,name='cancel_booking'),
    path('status/<int:booking_id>/',views.status,name='status'),
    path('delivery_date/<int:booking_id>/',views.delivery_date,name='delivery_date'),
    path('viewrequest/',views.viewrequest,name='viewrequest'),
    path('approve/<int:car_id>/',views.approve,name='approve'),
    path('reject/<int:car_id>/',views.reject,name='reject'),
    path('sellers/',views.sellers,name='sellers'),
    path('delete/<int:seller_id>/',views.delete,name='delete'),
    path('adminbookings/',views.adminbookings,name='adminbookings'),
    path('alogout/',views.alogout,name='alogout'),
    path('sendsellercomplaint/',views.sendsellercomplaint,name='sendsellercomplaint'),
    path('sendusercomplaint/',views.sendusercomplaint,name='sendusercomplaint'),
    path('mycars/',views.mycars,name='mycars'),
    path('updatecar/<int:car_id>/',views.updatecar,name='updatecar'),
    path('deletecar/<int:car_id>/',views.deletecar,name='deletecar'),
    path('complaints/',views.complaints,name='complaints'),
    path('sellerprofile/',views.sellerprofile,name='sellerprofile'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('review/<int:car_id>/',views.review,name='review'),
     path('payment/',views.payment,name='payment'),
  path('sharereferral/',views.sharereferral,name='sharereferral'),
  path('buy_with_referral/<int:car_id>/<str:referral_code>/', views.buy_with_referral, name='buy_with_referral'),

]
