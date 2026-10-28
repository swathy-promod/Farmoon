from django.urls import path
from .import views
app_name='Administrator'

urlpatterns = [
    path('District/',views.district,name='District'),
    path('Category/',views.category,name='Category'),
    path('Place/',views.place,name='Place'),
    path('placedelete/<int:id>/',views.placedelete, name = "placedelete"),
    path('editplace/<int:id>/',views.editplace, name="editplace"),
    path('Subcategory/',views.subcategory,name='Subcategory'),
    path('Subcategorydelete/<int:id>/',views.subcategorydelete, name = "Subcategorydelete"),
    path('editsubcategory/<int:id>/',views.editsubcategory, name="Editsubcategory"),
    path('AdminRegistration/',views.adminregistration,name='AdminRegistration'),
    path('districtdelete/<int:id>/',views.districtdelete, name = "districtdelete"),
    path('admindelete/<int:id>/',views.admindelete, name = "admindelete"),
    path('editadmin/<int:id>/',views.editadmin, name = "editadmin"),
    path('editdistrict/<int:id>/',views.editdistrict, name="editdistrict"),
    path('categorydelete/<int:id>/',views.categorydelete, name = "categorydelete"),
    path('editcategory/<int:id>/',views.editcategory, name="categoryedit"),
    path('HomePage/',views.HomePage, name="HomePage"),
    path('Userlist/',views.userlist, name="Userlist"),
    path('Farmerlist/',views.farmerlist, name= "Farmerlist"),
    path("accuser/<int:uid>/",views.useraccept,name = "accuser"),
    path("rejuser/<int:uid>/",views.userrej,name = "rejuser"),
    path("accfarmer/<int:uid>/",views.farmeraccept,name = "accfarmer"),
    path("rejfarmer/<int:uid>/",views.farmerrej,name = "rejfarmer"),
    path("ViewComplaint/",views.viewcomplaint,name = "ViewComplaint"),
    path("ViewFeedback/",views.viewfeedback,name = "ViewFeedback"),
    path("Reply/<int:uid>/",views.reply,name = "ReplyComplaint"),
    path("OrderList/",views.OrderList,name="OrderList"),
    path("OrderDetails/<int:id>/",views.orderdetails,name="OrderDetails"),
    path("TransactionList/",views.TransactionList,name="TransactionList"),
    path("TransactionDetails/<int:id>/",views.transactiondetails,name="TransactionDetails"),
    path("ExportOrders/",views.ExportOrders,name="ExportOrders"),    
    path("ExportTransactions/",views.ExportTransactions,name="ExportTransactions"),
    
]