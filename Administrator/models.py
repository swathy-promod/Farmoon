from django.db import models

class tbl_district(models.Model):
    district_name = models.CharField(max_length=100)

class tbl_adminregistration(models.Model):
    adminregistration_name = models.CharField(max_length=50)
    adminregistration_email = models.CharField(max_length=50)
    adminregistration_password = models.CharField(max_length=50)

class tbl_category(models.Model):
    category_name = models.CharField(max_length=30)

class tbl_place(models.Model):
    place_name = models.CharField(max_length=30)
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE,null=True,blank=True)

class tbl_subcategory(models.Model):
    subcategory_name = models.CharField(max_length=30)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE,null=True,blank=True)

