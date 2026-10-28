from django.urls import path
from .import views
app_name='Farmer'

urlpatterns = [
    path('ChangePassword/',views.changepassword,name= "ChangePassword"),
    path('EditProfile/',views.editprofile,name= "EditProfile"),
    path('MyProfile/',views.myprofile,name= "MyProfile"),
    path('HomePage/',views.homepage, name= "HomePage"),
    path('AddProduct/',views.addproduct, name= "AddProduct"),
    path('productdelete/<int:id>/',views.productdelete, name = "productdelete"),
    path('Stock/<int:pid>/',views.stock,name = "Stock"),
    path('Stockdelete/<int:id>/<int:pid>',views.stockdelete,name = "Stockdelete"),
    path('Gallery/<int:pid>',views.gallery, name="Gallery"),
    path('Viewbooking/',views.viewbooking,name='Viewbooking'),
     path('Orderpack/<int:oid>/',views.orderpack,name='Orderpack'),
    path('Ordershipped/<int:sid>/',views.ordershipped,name='Ordershipped'),
    path('Outfordelivery/<int:lid>/',views.outfordelivery,name='Outfordelivery'),
    path('Delivered/<int:vid>/',views.delivered,name='Delivered'),
    path('Viewrating/',views.viewrating,name= "Viewrating"),
    path('CropRecommend/',views.croprecommend,name="CropRecommend"),
    path('SalesReport/', views.SalesReport, name='SalesReport'),
]