from django.urls import path
from .import views
app_name='User'
urlpatterns = [
    path('ChangePassword/', views.changepassword, name='ChangePassword'),
    path('EditProfile/', views.editprofile, name='EditProfile'),
    path('HomePage/',views.homepage, name= "HomePage"),
    path('MyProfile/',views.myprofile, name= "MyProfile"),
    path('Complaint/',views.complaint, name= "Complaint"),
    path('Feedback/',views.feedback, name= "Feedback"),
    path('delcomplaint/<int:uid>/',views.delcomplaint, name= "delcomplaint"),
    
    path('Viewproduct/<int:fid>',views.Viewproduct,name='Viewproduct'),
    path('Addtocart/<int:pid>/<int:fid>/',views.Addtocart,name='Addtocart'),
    path('Viewmore/<int:pid>',views.Viewmore,name='Viewmore'),
    path('Mycart/',views.Mycart,name='Mycart'),
    path('CartQty/',views.CartQty,name='CartQty'),
    path('Payment/',views.payment,name='Payment'),
    path('Mybooking/',views.mybooking,name='Mybooking'),
    path('delcart/<int:did>',views.delcart,name='delcart'),
    path('User/cancel-booking/<int:cart_id>/', views.cancel_booking, name='cancel_booking'),

    path('rating/<int:mid>',views.rating,name="rating"),  
    path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
    path('starrating/',views.starrating,name="starrating"),
    path('ViewFarmers/',views.ViewFarmers,name="ViewFarmers"),
]