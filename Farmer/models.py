from django.db import models
from Administrator.models import *
from Guest.models import *

# Create your models here.
class tbl_product(models.Model):
    product_name= models.CharField(max_length=100)
    product_details= models.CharField(max_length=100)
    product_price= models.CharField(max_length=100)
    product_photo= models.FileField(upload_to = 'Assets/User/Photos/')
    category_id= models.ForeignKey(tbl_category,on_delete=models.CASCADE,null=True,blank=True)
    farmer_id= models.ForeignKey(tbl_farmerregistration,on_delete=models.CASCADE,null=True,blank=True)

class tbl_stock(models.Model):
    stock_quantity=  models.CharField(max_length=100)
    stock_date= models.DateField(auto_now=True)
    product_id= models.ForeignKey(tbl_product,on_delete=models.CASCADE,null=True,blank=True)

class tbl_gallery(models.Model):
    gallery_photo= models.FileField(upload_to = 'Assets/User/Photos/')
    product_id= models.ForeignKey(tbl_product,on_delete=models.CASCADE,null=True,blank=True)

