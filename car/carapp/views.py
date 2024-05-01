import uuid
from django.conf import settings
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse

from carapp.forms import CarUpdateForm,ProfileUpdateForm
from .models import Cars, Referral, User,Booking,Complaint,Review
from django.contrib import messages,auth
from django.db.models import Q
import razorpay
# Create your views here.


def index(request):
    return render(request,'index.html')



def home(request):
    query = request.GET.get('q')
    referral_code = request.GET.get('referral_code')

    if query:
        cars = Cars.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query) | Q(seller__name__icontains=query), is_approved=True)
    else:
        cars = Cars.objects.filter(is_approved=True)
   
       
    return render(request,'home.html',{'cars':cars})

def login(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        password=request.POST.get('password')
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            if user.is_buyer:
                auth.login(request,user)
                return redirect('home')
        else:
            messages.info(request,"invalid entry")
    return render(request,'login.html')


def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        phno=request.POST.get('phno')
        password=request.POST.get('password')
        cpass=request.POST.get('cpassword')

            
        if password==cpass:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"username already taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
            else:
                user=User.objects.create_user(name=name,username=uname,email=email,phone_number=phno,password=password,is_buyer=True)
                user.save()
                return render(request,'login.html')
        else:
            messages.info(request,"password not matching")
    return render(request,'register.html')



def slogin(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        password=request.POST.get('password')
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            if user.is_seller:
                auth.login(request,user)
                return redirect('sindex')
        else:
            messages.info(request,"invalid entry")
    return render(request,'seller/slogin.html')


def sregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        uname=request.POST.get('uname')
        email=request.POST.get('email')
        phno=request.POST.get('phno')
        password=request.POST.get('password')
        cpass=request.POST.get('cpassword')

            
        if password==cpass:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"username already taken")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
            else:
                user=User.objects.create_user(name=name,username=uname,email=email,phone_number=phno,password=password,is_seller=True)
                user.save()
                return render(request,'seller/slogin.html')
        else:
            messages.info(request,"password not matching")
    return render(request,'seller/sregister.html')


def sindex(request):
    cars=Cars.objects.filter(is_approved=True)
    return render(request,'seller/sindex.html',{'cars':cars})

def addcar(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        name = request.POST.get('name')
        mileage = request.POST.get('mileage')
        price = request.POST.get('price')
        location = request.POST.get('location')
        description = request.POST.get('desc')
        registration_year = request.POST.get('regy')
        registration_number = request.POST.get('regn')
        engine_capacity = request.POST.get('enc')
        insurance = request.POST.get('ins')
        spare_key = request.POST.get('spare')
        transmission = request.POST.get('trans')
        fuel_type = request.POST.get('fuel')
        img=request.FILES.get('img')

        car = Cars.objects.create(
            seller=request.user,
            brand=brand,
            name=name,
            mileage=mileage,
            price=price,
            location=location,
            description=description,
            registration_year=registration_year,
            registration_number=registration_number,
            engine_capacity=engine_capacity,
            insurance=insurance,
            spare_key=spare_key,
            transmission=transmission,
            fuel_type=fuel_type,
            img=img
        )
        car.save()
        return redirect('sindex')
    return render(request,'seller/add_car.html')


def car_detail(request,car_id):
    car=Cars.objects.get(id=car_id)
    reviews=Review.objects.filter(car=car)
    referrals=Referral.objects.filter(referred_user=request.user)

    return render(request,'car_detail.html',{'car':car,'reviews':reviews,'referrals':referrals})


def mycar_detail(request,car_id):
    car=Cars.objects.get(id=car_id)
    reviews=Review.objects.filter(car=car)
    return render(request,'seller/mycar_detail.html',{'car':car,'reviews':reviews})


def slogout(request):
    auth.logout(request)
    return render(request,'seller/slogin.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


# def buy_now(request, car_id):
#     car = get_object_or_404(Cars, id=car_id)
#     referrals = Referral.objects.all()
#     if request.method == 'POST':
#         user = request.user
#         booking = Booking(user=user, car=car)
#         booking.save()
        
#         referral_code = request.GET.get('referral_code')
#         if referral_code:
#             try:
#                 referred_user = User.objects.get(referral_code=referral_code)
#                 if referred_user != request.user: 
#                     referred_user.reward += 10
#                     referred_user.save()
#                     messages.success(request, f'Referrer {referred_user.username} rewarded!')
#                     referral = Referral(referrer=referred_user, referred_user=user, referral_code=referral_code)
#                     referral.save()
#             except User.DoesNotExist:
#                 pass  
        
#         return render(request, 'payment.html', {'booking': booking})
#     else:
#         return render(request, 'payment.html', {'car': car, 'referrals': referrals})

def buy_now(request, car_id):
    car = Cars.objects.get(pk=car_id)
    if request.method == 'POST':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_amount = int(car.price * 100)  # Convert to paisa
        payment_data = {
            'amount': payment_amount,
            'currency': 'INR',
            'receipt': 'booking_receipt',
            'payment_capture': 1
        }
        payment = client.order.create(data=payment_data)
        booking = Booking.objects.create(user=request.user, car=car)
        booking.payment_status = True  
        booking.save()
        return redirect('payment')
    return render(request, 'buy_now.html', {'car': car})


def buy_with_referral(request, car_id, referral_code):
    car = Cars.objects.get(pk=car_id)
    referral = Referral.objects.get(referral_code=referral_code)
    if request.method == 'POST':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_amount = int(car.price * 100)  
        payment_data = {
            'amount': payment_amount,
            'currency': 'INR',
            'receipt': 'booking_receipt',
            'payment_capture': 1
        }
        payment = client.order.create(data=payment_data)
        booking = Booking.objects.create(user=request.user, car=car)
        booking.payment_status = True  
        booking.save()
        referrer = referral.referrer
        if referrer.reward is None:  
            referrer.reward = 0  
        referrer.reward += 100
        referrer.save()
        return redirect('payment')
    return render(request, 'buy_with_referral.html', {'car': car, 'referral_code': referral_code})



def payment(request):
    if request.method == "POST":
        razorpay_client = razorpay.Client(auth=("rzp_test_xgNFQhsqKotruM", "iZM2W0VsYG7mvyY2kKPdcPbO"))

        # Fetch parameters from POST request
        amount = int(request.POST['amount']) * 100  # Amount in paise
        currency = 'INR'
        receipt = 'receipt_' + str(uuid.uuid4())[:8]

        # Create order
        order = razorpay_client.order.create({
            'amount': amount,
            'currency': currency,
            'receipt': receipt,
            # Add other parameters as needed
        })

        
    return render(request, 'payment.html')

def adminlogin(request):
    if request.method=='POST':
        uname=request.POST.get('uname')
        password=request.POST.get('password')
        user=auth.authenticate(username=uname,password=password)
        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect('aindex')
        else:
            messages.info(request,"invalid entry")
    return render(request,'admin/alogin.html')


def aindex(request):
    return render(request,'admin/aindex.html')


def sellerbookings(request):
    cars_listed_by_seller = Cars.objects.filter(seller=request.user)
    bookings = Booking.objects.filter(car__in=cars_listed_by_seller).order_by('-id')
    return render(request,'seller/bookings.html',{'bookings':bookings})


def bookings(request):
    bookings=Booking.objects.filter(user=request.user).order_by('-id')
    return render(request,'bookings.html',{'bookings':bookings})


def cancel_booking(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    booking.delete()
    return redirect('bookings')

def status(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    booking.status='Completed'
    booking.save()
    return redirect('sellerbookings')


def delivery_date(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    if request.method=='POST':
        deliverydate=request.POST.get('ddate')
        booking.delivery_date=deliverydate
        booking.save()
    return redirect('sellerbookings')\
    
def viewrequest(request):
    cars=Cars.objects.filter(is_approved=False)
    return render(request,'admin/request.html',{'cars':cars})


def approve(request,car_id):
    car=Cars.objects.get(id=car_id)
    car.is_approved=True
    car.save()
    return redirect('viewrequest')

def reject(request,car_id):
    car=Cars.objects.get(id=car_id) 
    car.is_rejected=True
    car.save()
    return redirect('viewrequest')

def sellers(request):
    sellers=User.objects.filter(is_seller=True)
    return render(request,'admin/sellers.html',{'sellers':sellers})

def delete(request,seller_id):
    seller=User.objects.get(id=seller_id)
    seller.delete()
    return redirect('sellers')


def adminbookings(request):
    bookings=Booking.objects.all()
    return render(request,'admin/bookings.html',{'bookings':bookings})

def alogout(request):
    auth.logout(request)
    return render(request,'admin/alogin.html')

def sendsellercomplaint(request):
    if request.method=='POST':
        user=request.user
        complaint=request.POST.get('complaint')
        com=Complaint(user=user,complaint=complaint)
        com.save()
    return redirect('sindex')


def sendusercomplaint(request):
    if request.method=='POST':
        user=request.user
        complaint=request.POST.get('complaint')
        com=Complaint(user=user,complaint=complaint)
        com.save()
    return redirect('home')

def mycars(request):
    seller=request.user
    cars=Cars.objects.filter(seller=seller)
    return render(request,'seller/mycars.html',{'cars':cars})

def updatecar(request, car_id):
    car = Cars.objects.get(id=car_id)
    if request.method == 'POST':
        form = CarUpdateForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('mycar_detail',car_id=car_id)  
    else:
        form = CarUpdateForm(instance=car)
    return render(request, 'seller/updatecar.html', {'form': form})


def deletecar(request,car_id):
    car = get_object_or_404(Cars, id=car_id)
    car.delete()
    return redirect('mycars')

def complaints(request):
    complaints=Complaint.objects.all()
    return render(request,'admin/complaints.html',{'complaints':complaints})


def sellerprofile(request):
    seller=request.user
    if request.method=='POST':
        form =ProfileUpdateForm(request.POST,instance=seller)
        if form.is_valid():
            form.save()
            return redirect('sellerprofile')
    else:
        form=ProfileUpdateForm(instance=seller)
    return render(request,'seller/profile.html',{'form':form})

def userprofile(request):
    user=request.user
    users=User.objects.filter(is_buyer=True)
    if request.method=='POST':
        form =ProfileUpdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile')
    else:
        form=ProfileUpdateForm(instance=user)
    return render(request,'profile.html',{'form':form,'users':users})


def review(request,car_id):
    car=Cars.objects.get(id=car_id)
    user=request.user
    if request.method=='POST':
        review=request.POST.get('review')
        r=Review(user=user,car=car,review=review)
        r.save()
    return redirect('car_detail',car_id=car_id)


def payment(request):
    return render(request,'payment.html')

def sharereferral(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        receiver = User.objects.get(id=user_id)
        code=request.POST.get('r')
        sender = request.user
        referral = Referral(referrer=sender, referred_user=receiver,referral_code=code)
        referral.save()
    return redirect('userprofile')  
   
