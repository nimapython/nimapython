import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    name=models.CharField(max_length=200)
    username=models.CharField(max_length=20, unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=20)
    phone_number=models.BigIntegerField(null=True)
    referral_code = models.CharField(max_length=10, unique=True, null=True)
    reward=models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8].replace('-', '').upper() # Generate unique referral code
        super().save(*args, **kwargs)

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_user')
    referral_code = models.CharField(max_length=10, unique=True)



class Cars(models.Model):
    seller=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    mileage = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    description = models.TextField()
    registration_year = models.DateField()
    registration_number = models.CharField(max_length=20)
    engine_capacity = models.FloatField()
    insurance = models.DecimalField(max_digits=10, decimal_places=2)
    spare_key = models.BooleanField(default=False)
    transmission = models.CharField(max_length=20)
    fuel_type = models.CharField(max_length=20)
    img=models.ImageField(upload_to='cars',null=True)
    is_approved=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    @property
    def imageURL(self):
        if self.img:
            return self.img.url
        else:
            return ''

    
class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    car=models.ForeignKey(Cars, on_delete=models.CASCADE,null=True)
    booking_date = models.DateTimeField(default=timezone.now,null=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status=models.BooleanField(default=False)


class Complaint(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    complaint=models.TextField()


class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    car=models.ForeignKey(Cars,on_delete=models.CASCADE)
    review=models.TextField()


def generate_referral_code(sender, instance, created, **kwargs):
    if created and instance.is_buyer:
        instance.referral_code = str(uuid.uuid4())[:8].replace('-', '').upper()
        instance.save()