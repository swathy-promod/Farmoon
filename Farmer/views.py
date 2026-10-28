from django.shortcuts import render,redirect
from Guest.models import*
from User.models import*

from Farmer.models import *
from Administrator.models import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.db.models import Avg

# Create your views here.
import os
import pandas as pd
import joblib  # Import joblib to load the model

# Create your views here.
def changepassword(request):
    return render(request,'Farmer/ChangePassword.html')

def editprofile(request):
    return render(request,'Farmer/EditProfile.html')

def myprofile(request):
    data=tbl_farmerregistration.objects.get(id=request.session["fid"])
    return render(request,'Farmer/MyProfile.html',{'data':data})

def homepage(request):
    return render(request,'Farmer/HomePage.html')

def editprofile(request):
    data=tbl_farmerregistration.objects.get(id=request.session["fid"])
    if request.method =='POST':
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        contact = request.POST.get("num_contact")
        address = request.POST.get("txt_Address")

        data.farmer_name = name
        data.farmer_email = email
        data.farmer_contact = contact
        data.farmer_address = address
        data.save()
        return render(request,'Farmer/MyProfile.html',{'Msg':"Profile Updated"})   
    else:
        return render(request,'Farmer/EditProfile.html',{'data':data})

def changepassword(request):
    user=tbl_farmerregistration.objects.get(id=request.session['fid'])
    if request.method=='POST':
        old_password = request.POST.get("txt_password")
        new_password = request.POST.get("txt_newpassword")
        retype_password = request.POST.get("txt_retypepassword")
        if user.farmer_password==old_password:
            if new_password == retype_password:
                user.farmer_password = new_password
                user.save()
                return render(request,"Farmer/MyProfile.html",{"Msg":"Password changed successfully"})
            else:    
                return render(request,'Farmer/ChangePassword.html',{"Msg":"New Password do not match"})
        else:
            return render(request,"Farmer/ChangePassword.html",{"Msg":"Old Password Incorrect"})
    else:
        return render(request,"Farmer/ChangePassword.html")



def addproduct(request):
    product_data= tbl_product.objects.all()
    category_data = tbl_category.objects.all()
    farmer=tbl_farmerregistration.objects.get(id=request.session['fid'])
    if request.method =='POST':
        p_name= request.POST.get("txt_name")
        p_details= request.POST.get("txt_details")
        p_price= request.POST.get("num_price")
        p_photo= request.FILES.get('file_photo')
        category=request.POST.get("sel_category")
        category_obj=tbl_category.objects.get(id=category)
        tbl_product.objects.create(product_name=p_name,product_details=p_details,product_price=p_price,
                                            product_photo=p_photo,category_id=category_obj,farmer_id=farmer)
        return redirect("Farmer:AddProduct")
    else:
        return render(request,'Farmer/AddProduct.html',{'addproduct':product_data,'category':category_data})

def productdelete(request, id):
    tbl_product.objects.get(id=id).delete()
    return redirect("Farmer:AddProduct")

def stock(request, pid):
    product = tbl_product.objects.get(id=pid)
    stock_data = tbl_stock.objects.filter(product_id=pid)
    if request.method =='POST':
        stock_q = request.POST.get("num_quantity")
        tbl_stock.objects.create(
            stock_quantity=stock_q,
            product_id=product,
            )
        return render(request,"Farmer/Stock.html",{'msg':"Data inserted", 'pid':pid})
    else:
        return render(request,'Farmer/Stock.html',{
        'stock': stock_data,
        'product': product,                              # pass product to template
        'pid': pid,
    })

def stockdelete(request, id,pid):
    tbl_stock.objects.get(id=id).delete()
    return redirect("Farmer:Stock",pid)

def gallery(request, pid):
    gallery_data = tbl_gallery.objects.all()
    if request.method =='POST':
        photo = request.POST.get("file_photo")
        tbl_gallery.objects.create(
            gallery_photo=photo,
            product_id=tbl_product.objects.get(id=pid),
        )
        return redirect("Farmer:Gallery")
    else:
        return render(request,'Farmer/Gallery.html',{'photo':gallery_data, 'pid':pid})    
            
def viewbooking(request):
    
    bookingdata=tbl_booking.objects.filter(tbl_cart__productid__farmer_id=request.session['fid'],booking_status__gt=1)
    return render(request,'Farmer/Viewbooking.html',{'bookingdata':bookingdata})

def orderpack(request,oid):
    orderdata=tbl_cart.objects.filter(bookingid=oid).update(cart_status=3)
    return redirect('Farmer:Viewbooking')

def ordershipped(request,sid):
    shippeddata=tbl_cart.objects.filter(bookingid=sid).update(cart_status=4)
    return redirect('Farmer:Viewbooking')

def outfordelivery(request,lid):
    outdata=tbl_cart.objects.filter(bookingid=lid).update(cart_status=5)
    return redirect('Farmer:Viewbooking')

def delivered(request,vid):
    deldata=tbl_cart.objects.filter(bookingid=vid).update(cart_status=6)
    bookingdata=tbl_booking.objects.get(id=vid)
    bookingdata.booking_status=6
    bookingdata.save()
    email=bookingdata.userid.userregistration_email
    send_mail(
        'Order Delivered Successfully',
        "Hello " + str(bookingdata.userid.userregistration_name) + ",\n\n"
        "Good news! Your order has been successfully delivered.\n\n"
        "We hope you are satisfied with the products you received from our Farmer Product Selling & Crop Recommendation System.\n\n"
        "Thank you for shopping with us. We look forward to serving you again.\n\n"
        "Best regards,\n"
        "Farmer Product Selling & Crop Recommendation System Team",
        settings.EMAIL_HOST_USER,
        [email],
    )
    return redirect('Farmer:Viewbooking')

def viewrating(request):
    farmer = tbl_farmerregistration.objects.get(id=request.session['fid'])
    ratings = tbl_rating.objects.filter(farmer=farmer)
    average = ratings.aggregate(Avg('rating_data'))['rating_data__avg']

    return render(request, "Farmer/ViewRating.html", {
        "ratings": ratings,
        "average": average
    })


# Define the correct model path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Get project base directory
MODEL_PATH = os.path.join(BASE_DIR, 'Assets', 'Model', 'knn_model.pkl')  # Correct model path

# Load the model
model = joblib.load(MODEL_PATH)

def croprecommend(request):
    if request.method == 'POST':
        # Get input values from the form
        nitrogen = float(request.POST['nitrogen'])
        potassium = float(request.POST['potassium'])
        temperature = float(request.POST['temperature'])
        humidity = float(request.POST['humidity'])
        rainfall = float(request.POST['rainfall'])
        soiltype = int(request.POST['soiltype']) 
        print(soiltype)
        soil_depth = float(request.POST['soil_depth'])

        # Create DataFrame for model prediction
        input_data = pd.DataFrame({
            'N': [nitrogen],
            'K': [potassium],
            'temperature': [temperature],
            'humidity': [humidity],
            'rainfall': [rainfall],
            'soiltype': [soiltype],
            'Soil_Depth_cm': [soil_depth]
        })

        # Make prediction
        prediction = model.predict(input_data)
        recommended_crop = prediction[0]

        return render(request, 'Farmer/CropRecommendation.html', {'res': recommended_crop})

    return render(request, 'Farmer/CropRecommendation.html')

def SalesReport(request):
    fid = request.session.get('fid')  # FIXED: was 'farmer_id'

    # All products belonging to this farmer
    farmer_products = tbl_product.objects.filter(farmer_id=fid)

    # All cart items for those products that have a booking
    cart_items = tbl_cart.objects.filter(
        productid__in=farmer_products,
        bookingid__isnull=False
    ).select_related('productid', 'bookingid', 'bookingid__userid')

    # Summary stats
    total_orders   = cart_items.count()
    total_revenue  = sum(
        int(item.cart_quantity) * int(item.productid.product_price)
        for item in cart_items
    )
    total_products = farmer_products.count()
    delivered      = cart_items.filter(cart_status=6).count()

    return render(request, 'Farmer/SalesReport.html', {
        'cart_items'    : cart_items,
        'total_orders'  : total_orders,
        'total_revenue' : total_revenue,
        'total_products': total_products,
        'delivered'     : delivered,
    })
