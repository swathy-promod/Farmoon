from django.shortcuts import render,redirect
from Guest.models import *
from Administrator.models import *
from Farmer.models import *
from Guest.models import tbl_farmerregistration
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def login(request):
    if request.method == "POST":
        email=request.POST.get('txt_Email')
        password=request.POST.get('txt_password')
        usercount=tbl_userregistration.objects.filter(
            userregistration_email=email,userregistration_password=password
            ).count()
        admincount=tbl_adminregistration.objects.filter(
            adminregistration_email=email,adminregistration_password=password
            ).count()
        farmercount=tbl_farmerregistration.objects.filter(
            farmer_email=email,farmer_password=password
            ).count()
        if usercount > 0:
            userdata = tbl_userregistration.objects.get(
                userregistration_email=email,userregistration_password=password
                )
            if userdata.user_status == 0:
                return render(request,'Guest/Login.html',{"Msg":"Registration Pending"})
            elif userdata.user_status == 2:
                return render(request,'Guest/Login.html',{"Msg":"Registration Rejected"})
            else:
                request.session["uid"] = userdata.id
                return redirect("User:HomePage")
        elif admincount > 0:
            admindata = tbl_adminregistration.objects.get(
                adminregistration_email=email,adminregistration_password=password
                )
            request.session["aid"] = admindata.id
            return redirect("Administrator:HomePage")
        elif farmercount > 0:
            farmerdata = tbl_farmerregistration.objects.get(
                farmer_email=email,farmer_password=password
                )
            request.session["fid"] = farmerdata.id
            return redirect("Farmer:HomePage")
        else:
            return render(request,'Guest/Login.html',{"Msg":"Invalid Email or Password"})
    else:
        return render(request,'Guest/Login.html')

def userregistration(request):
    userregistration_data=tbl_userregistration.objects.all()
    district_data=tbl_district.objects.all()
    place_data=tbl_place.objects.all()
    if request.method == "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_Email')
        contact=request.POST.get('num_contact')
        address=request.POST.get('txt_Address')
        gender=request.POST.get('rd_Gender')
        dateofbirth=request.POST.get('txt_date')
        district_id=request.POST.get("sel_district")
        district_obj=tbl_district.objects.get(id=district_id)
        place_id=request.POST.get("txt_place")
        place_obj=tbl_place.objects.get(id=place_id)
        photo=request.FILES.get('file_photo')
        password=request.POST.get('txt_password')
        tbl_userregistration.objects.create(userregistration_name=name,userregistration_email=email,userregistration_contact=contact,
                                            userregistration_address=address,userregistration_gender=gender,userregistration_dateofbirth=dateofbirth,
                                            userregistration_place=place_obj,userregistration_photo=photo,userregistration_password=password)
        return redirect("Guest:UserRegistration")
    else:
        return render(request,'Guest/UserRegistration.html',{'userregistration':userregistration_data,'district':district_data,'place':place_data})

def ajaxplace (request):
    place=tbl_place.objects.filter(district=request.GET.get('did'))
    return render(request,'Guest/Ajaxplace.html',{'place':place})

def farmerregistration(request):
    farmerregistration_data= tbl_farmerregistration.objects.all()
    district_data=tbl_district.objects.all()
    place_data=tbl_place.objects.all()
    if request.method == "POST":
        name=request.POST.get('txt_name')
        email=request.POST.get('txt_Email')
        contact=request.POST.get('num_contact')
        address=request.POST.get('txt_Address')
        district_id=request.POST.get("sel_district")
        district_obj=tbl_district.objects.get(id=district_id)
        place_id=request.POST.get("txt_place")
        place_obj=tbl_place.objects.get(id=place_id)
        photo=request.FILES.get('file_photo')
        proof=request.FILES.get('file_proof')
        password=request.POST.get('txt_password')
        tbl_farmerregistration.objects.create(farmer_name=name,farmer_email=email,farmer_contact=contact,
                                            farmer_address=address,place_id=place_obj,farmer_photo=photo,farmer_proof=proof,farmer_password=password)
        return redirect("Guest:FarmerRegistration")
    else:
        return render(request,'Guest/FarmerRegistration.html',{'farmerregistration':farmerregistration_data,'district':district_data,'place':place_data})


def index(request):
    product_data= tbl_product.objects.all()
    category_data = tbl_category.objects.all()
    return render(request,"Guest/index.html",{'addproduct':product_data,'category':category_data})


def aboutus(request):
    return render(request,"Guest/AboutUs.html")


def contactus(request):
    return render(request,"Guest/ContactUs.html")
    
def product(request):
    all_products = tbl_product.objects.all()       # fetches every farmer's products
    categories   = tbl_category.objects.all()      # for the filter tabs
    return render(request, 'Guest/Product.html', {
        'all_products': all_products,
        'categories': categories,
    })


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        user = tbl_userregistration.objects.filter(userregistration_email=email).count()
        farmer = tbl_farmerregistration.objects.filter(farmer_email=email).count()
        admin = tbl_adminregistration.objects.filter(adminregistration_email=email).count()
        otp = random.randint(111111,999999)
        request.session["otp"] = otp
        if user > 0:
            userdata=tbl_userregistration.objects.get(userregistration_email=email)
            request.session["usid"] = userdata.id
            send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
            return render(request,"Guest/ForgotPassword.html",{"msg":email})

        elif farmer > 0:
            farmerdata = tbl_farmerregistration.objects.get(farmer_email=email)
            request.session["fsid"] = farmerdata.id   
            send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
            return render(request,"Guest/ForgotPassword.html",{"msg":email})

        elif admin > 0:
            admindata = tbl_adminregistration.objects.get(adminregistration_email=email)
            request.session["aid"] = admindata.id  
            send_mail(
            'Forgot password OTP', #subject
            "\rHello \r" + str(otp) +"\n This is the OTP to reset ur password.\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
            return render(request,"Guest/ForgotPassword.html",{"msg":email})
    
        else:
            return render(request,"Guest/ForgotPassword.html",{"msg":"invalid email id"})
 
        
    else:
        return render(request,"Guest/ForgotPassword.html")

def otp(request):
    if request.method == "POST":
        inp_otp = int(request.POST.get("txt_otp"))
        if inp_otp == request.session["otp"]:
            return redirect("Guest:newpass")
        else:
            return render(request,"Guest/OTP.html",{"msg":"OTP Does not Matches..!!"})
    else:
        return render(request,"Guest/OTP.html")

def newpassword(request):
    if request.method == "POST":
        if request.POST.get("txt_new_pass") == request.POST.get("txt_con_pass"):
            if 'usid' in request.session:
                user = tbl_userregistration.objects.get(id=request.session["usid"])
                user.userregistration_password = request.POST.get("txt_con_pass")
                user.save()
                del request.session['usid']
                return render(request,"Guest/NewPassword.html",{"msg1":"Password Updated Sucessfully...."})
            elif 'fsid' in request.session:
                farmer = tbl_farmerregistration.objects.get(id=request.session["fsid"])
                farmer.farmer_password = request.POST.get("txt_con_pass")
                farmer.save()
                del request.session['fsid']
                return render(request,"Guest/NewPassword.html",{"msg1":"Password Updated Sucessfully...."})
            elif 'aid' in request.session:
                admin = tbl_adminregistration.objects.get(id=request.session["aid"])
                admin.adminregistration_password = request.POST.get("txt_con_pass")
                admin.save()
                del request.session['aid']
                return render(request,"Guest/NewPassword.html",{"msg1":"Password Updated Sucessfully...."})
        else:
            return render(request,"Guest/NewPassword.html",{"msg":"Error in confirm password..!!!"})
    else:
        return render(request,"Guest/NewPassword.html")