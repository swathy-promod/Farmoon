from django.db import models
from Guest.models import*
from Farmer.models import *
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
from Guest.models import tbl_userregistration

class tbl_complaint(models.Model):
    complaint_title = models.CharField(max_length=100)
    complaint_content = models.CharField(max_length=100)
    complaint_date = models.DateField(auto_now=True)
    complaint_status = models.IntegerField(default = 0)
    complaint_reply = models.CharField(max_length=100)
    user = models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE,null=True,blank=True)

class tbl_feedback(models.Model):
    feedback_content = models.CharField(max_length=100)
    feedback_date = models.DateField(auto_now=True)
    feedback_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE,null=True,blank=True)

class tbl_booking(models.Model):
    booking_date= models.DateField(auto_now_add=True)
    booking_time = models.TimeField(auto_now_add=True)
    booking_status= models.IntegerField(default=0)
    booking_amount= models.CharField(max_length=60)
    userid=models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE,null=True)
    delivery_address = models.TextField(null=True, blank=True)
    
class tbl_cart(models.Model):
    cart_quantity= models.IntegerField(default=1)
    cart_status= models.IntegerField(default=0)
    productid=models.ForeignKey(tbl_product,on_delete=models.CASCADE,null=True)
    bookingid=models.ForeignKey(tbl_booking,on_delete=models.CASCADE,null=True)



class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user=models.ForeignKey(tbl_userregistration,on_delete=models.CASCADE)
    user_review=models.CharField(max_length=500)
    farmer=models.ForeignKey(tbl_farmerregistration,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)

class tbl_payment(models.Model):
    bookingid = models.ForeignKey(tbl_booking, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default="Online Payment")
    payment_status = models.CharField(max_length=20, default="Success")
    payment_date = models.DateTimeField(auto_now_add=True)