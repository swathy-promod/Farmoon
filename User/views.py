from django.shortcuts import render,redirect
from Guest.models import*
from Farmer.models import *
from User.models import *
from Administrator.models import*
from django.db.models import Sum
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import tbl_payment
import uuid
# Create your views here.
def changepassword(request):
    user=tbl_userregistration.objects.get(id=request.session['uid'])
    if request.method=='POST':
        old_password = request.POST.get("txt_password")
        new_password = request.POST.get("txt_newpassword")
        retype_password = request.POST.get("txt_retypepassword")
        if user.userregistration_password==old_password:
            if new_password == retype_password:
                user.userregistration_password = new_password
                user.save()
                return render(request,"User/MyProfile.html",{"Msg":"Password changed successfully"})
            else:    
                return render(request,'User/ChangePassword.html',{"Msg":"New Password do not match"})
        else:
            return render(request,"User/ChangePassword.html",{"Msg":"Old Password Incorrect"})
    else:
        return render(request,"User/ChangePassword.html")
def myprofile(request):
    data=tbl_userregistration.objects.get(id=request.session["uid"])
    return render(request,'User/MyProfile.html',{'data':data})

def homepage(request):
    return render(request,'User/HomePage.html')

def editprofile(request):
    data=tbl_userregistration.objects.get(id=request.session["uid"])
    if request.method =='POST':
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        contact = request.POST.get("txt_contact")
        address = request.POST.get("txt_Address")

        data.userregistration_name = name
        data.userregistration_email = email
        data.userregistration_contact = contact
        data.userregistration_address = address
        data.save()
        return render(request,'User/MyProfile.html',{'Msg':"Profile Updated"})   
    else:
        return render(request,'User/EditProfile.html',{'data':data})     

def complaint(request):
    complaintdata = tbl_complaint.objects.filter(user = request.session['uid'])
    if request.method == 'POST':
        title = request.POST.get("txt_title")
        content = request.POST.get("txt_content")

        tbl_complaint.objects.create(
            complaint_title=title,
            complaint_content=content,
            user=tbl_userregistration.objects.get(id=request.session['uid'])
        )
        return redirect("User:Complaint")
    else:
        return  render(request,'User/Complaint.html',{'complaint':complaintdata})

def feedback(request):
    feedbackdata = tbl_feedback.objects.filter(user = request.session['uid'])
    if request.method == 'POST':
        content = request.POST.get("txt_feedback")
        rating = request.POST.get("txt_rating")
        tbl_feedback.objects.create(
            feedback_content = content,
            feedback_rating = int(rating),
            user=tbl_userregistration.objects.get(id=request.session['uid'])
        )
        return redirect("User:HomePage")
    else:
        return render(request,"User/Feedback.html",{'feedback':feedbackdata})

def delcomplaint(request,uid):
    tbl_complaint.objects.get(id=uid).delete()
    return redirect("User:Complaint")

def Viewproduct(request,fid):
    Productdata=tbl_product.objects.filter(farmer_id=fid)
    return render(request,'User/Viewproduct.html',{'Productdata':Productdata,'fid':fid})

def Addtocart(request,pid,fid):
    productid=tbl_product.objects.get(id=pid)
    userdata=tbl_userregistration.objects.get(id=request.session['uid'])
    bookingcount=tbl_booking.objects.filter(userid=request.session['uid'],booking_status=0).count()
    if bookingcount>0:
        booking=tbl_booking.objects.get(userid=userdata,booking_status=0)
        cartcount=tbl_cart.objects.filter(bookingid=booking,productid=productid).count()
        if cartcount>0:
            return render(request,"User/Viewproduct.html",{'msg':"Already Added",'fid':fid})
        else:
            tbl_cart.objects.create(bookingid=booking,productid=productid)
            return render(request,"User/Viewproduct.html",{'msg':"Added To cart",'fid':fid})
    else:
        booking=tbl_booking.objects.create(userid=userdata)
        tbl_cart.objects.create(bookingid=booking,productid=productid)
        return render(request,'User/Viewproduct.html',{'msg':"Product added to cart",'fid':fid})
        
def Viewmore(request,pid):
    productdata=tbl_product.objects.get(id=pid)
    viewproduct=tbl_gallery.objects.filter(product_id=pid)
    return render(request,'User/Viewmore.html',{'productdata':productdata,'Viewproduct':viewproduct, 'fid': productdata.farmer_id.id})

def Mycart(request):
    userdata = tbl_userregistration.objects.get(id=request.session['uid'])

    if request.method == 'POST':
        bookingdata = tbl_booking.objects.get(id=request.session['booking'])

        bookingdata.booking_amount = request.POST.get("carttotalamt")
        bookingdata.delivery_address = request.POST.get("delivery_address")
        bookingdata.booking_status = 1

        bookingdata.save()

        cartdata = tbl_cart.objects.filter(bookingid=bookingdata)
        for i in cartdata:
            i.cart_status = 1
            i.save()

        return redirect('User:Payment')

    bookingcount = tbl_booking.objects.filter(
        userid=request.session['uid'],
        booking_status=0
    ).count()

    if bookingcount > 0:
        booking = tbl_booking.objects.get(userid=userdata, booking_status=0)
        request.session["booking"] = booking.id

        cart = tbl_cart.objects.filter(bookingid=booking)

        for i in cart:
            total_stock = tbl_stock.objects.filter(
                product_id=i.productid.id
            ).aggregate(total=Sum('stock_quantity'))['total']

            total_cart = tbl_cart.objects.filter(
                productid=i.productid.id,
                cart_status__gte=1
            ).aggregate(total=Sum('cart_quantity'))['total']

            if total_stock is None:
                total_stock = 0
            if total_cart is None:
                total_cart = 0

            i.total_stock = total_stock - total_cart

        return render(request, 'User/Mycart.html', {'cart': cart})

    return render(request, 'User/Mycart.html')

def CartQty(request):
    qty = request.GET.get("qty")
    cid = request.GET.get("cid")
    cart=tbl_cart.objects.get(id=cid)
    cart.cart_quantity=qty
    cart.save()
    return redirect("User:Mycart")

def delcart(request,did):
    tbl_cart.objects.get(id=did).delete()
    return redirect('User:Mycart')

def payment(request):
    bookingdata = tbl_booking.objects.get(id=request.session['booking'])

    if request.method == "POST":

        bookingdata.booking_status = 2
        bookingdata.save()

        cartdata = tbl_cart.objects.filter(bookingid=bookingdata)
        for i in cartdata:
            i.cart_status = 2
            i.save()

        # Save payment record
        tbl_payment.objects.create(
            bookingid=bookingdata,
            payment_amount=bookingdata.booking_amount,
            payment_method="Card",
            payment_status="Success",

        )
 
        send_mail(
            'Order Payment Successful',
            "Hello " + str(bookingdata.userid.userregistration_name) +
            ",\n\nYour payment has been completed successfully.\n\n"
            "Your order has been confirmed and is now being processed.\n\n"
            "Thank you for purchasing products from our Farmer Product Selling & Crop Recommendation System.\n\n"
            "Best regards,\nFarmer Product Selling & Crop Recommendation System Team",
            settings.EMAIL_HOST_USER,
            [bookingdata.userid.userregistration_email],
        )

        return redirect("User:Mybooking")

    return render(request, 'User/Payment.html', {'bookingdata': bookingdata})

def mybooking(request):
    bookingdata=tbl_booking.objects.filter(userid=request.session['uid'],booking_status__gt=0)
    return render(request,'User/Mybooking.html',{'bookingdata':bookingdata})

def cancel_booking(request, cart_id):
    cart = tbl_cart.objects.get(id=cart_id, bookingid__userid=request.session['uid'])

    # Allow cancel only before Out for Delivery (status 1,2,3,4)
    if cart.cart_status in [1, 2, 3, 4]:
        cart.cart_status = 7  # Cancelled
        cart.save()

    return redirect('User:Mybooking')

def rating(request, mid):
    stardata = tbl_rating.objects.filter(farmer=mid).order_by('-datetime').select_related('user')
    count = stardata.count()

    avg = 0
    if count > 0:
        total = sum(i.rating_data for i in stardata)
        avg = round(total / count, 1)

    return render(request, "User/Rating.html", {
        'mid': mid,
        'data': stardata,
        'avg': avg,
        'count': count,
    })

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    
    user_review=request.GET.get('user_review')
    pid=request.GET.get('pid')
    # wdata=tbl_booking.objects.get(id=pid)
    tbl_rating.objects.create(user=tbl_userregistration.objects.get(id=request.session['uid']),user_review=user_review,rating_data=rating_data,farmer=tbl_farmerregistration.objects.get(id=pid))
    stardata=tbl_rating.objects.filter(farmer=pid).order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    # cdata = tbl_booking.objects.get(id=request.GET.get("pdt"))
    rate = tbl_rating.objects.filter(farmer=request.GET.get("pdt"))
    ratecount = tbl_rating.objects.filter(farmer=request.GET.get("pdt")).count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
        # print(i.rating_data)
        # r_len = r_len + int(i.rating_data)
    # rlen = r_len // 5
    # print(rlen)
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)

def ViewFarmers(request):
    districtdata=tbl_district.objects.all()
    farmerdata=tbl_farmerregistration.objects.filter(farmer_status=1)
    if request.method == 'POST':
        district=request.POST.get("sel_district")
        place=request.POST.get("sel_place")
        if district :
            farmer = tbl_farmerregistration.objects.filter(farmer_status=1,place_id__district=district)
        if place :
            farmer = tbl_farmerregistration.objects.filter(farmer_status=1,place_id=place)
        return render(request, "User/ViewFarmers.html", {'farmerdata': farmer,'districtdata':districtdata,})
    else:
        return render(request,'User/ViewFarmers.html',{'districtdata':districtdata,'farmerdata':farmerdata})

