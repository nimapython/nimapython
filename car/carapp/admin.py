from django.contrib import admin
from .models import User,Cars,Referral,Booking,Complaint,Review
# Register your models here.
admin.site.register(User)
admin.site.register(Cars)
admin.site.register(Referral)
admin.site.register(Booking)
admin.site.register(Complaint)
admin.site.register(Review)
