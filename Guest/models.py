from django.db import models
from Administrator.models import *

# Create your models here.
class tbl_userregistration(models.Model):
    userregistration_name= models.CharField(max_length=100)
    userregistration_email= models.CharField(max_length=100)
    userregistration_contact= models.CharField(max_length=100)
    userregistration_address= models.CharField(max_length=100)
    userregistration_gender= models.CharField(max_length=100)
    userregistration_dateofbirth= models.DateField(max_length=100)
    userregistration_place= models.ForeignKey(tbl_place,on_delete=models.CASCADE,null=True,blank=True)
    userregistration_photo = models.FileField(upload_to = 'Assets/User/Photos/')
    userregistration_password= models.CharField(max_length=100)
    user_status = models.IntegerField(default = 0)
    
class tbl_farmerregistration(models.Model):
    farmer_name= models.CharField(max_length=100)
    farmer_email= models.CharField(max_length=100)
    farmer_contact= models.CharField(max_length=100)
    farmer_address= models.CharField(max_length=100)
    farmer_photo= models.FileField(upload_to = 'Assets/User/Photos/')
    farmer_proof= models.FileField(upload_to = 'Assets/User/Photos/')
    farmer_password= models.CharField(max_length=100)
    farmer_status= models.IntegerField(default = 0)
    place_id= models.ForeignKey(tbl_place,on_delete=models.CASCADE,null=True,blank=True)