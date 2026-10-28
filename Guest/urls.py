from django.urls import path
from .import views
app_name='Guest'
urlpatterns = [
    path('Login/', views.login, name='Login'),
    path('UserRegistration/', views.userregistration, name='UserRegistration'),
    path('Ajaxplace/',views.ajaxplace, name= "Ajaxplace"),
    path('FarmerRegistration/',views.farmerregistration,name ="FarmerRegistration"),
    path('', views.index, name='index'),
    path('AboutUs/', views.aboutus, name='AboutUs'),
    path('ContactUs/', views.contactus, name='ContactUs'),
    path('Product/', views.product, name='Product'),
    path('OTP/', views.otp, name='OTP'),
    path('ForgotPassword/', views.forgotpassword, name='ForgotPassword'),
    path('NewPassword/', views.newpassword, name='NewPassword'),
]