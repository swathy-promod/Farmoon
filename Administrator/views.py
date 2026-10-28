from django.shortcuts import render,redirect
from django.db.models import Sum
from .models import*
from Guest.models import*
from User.models import*
from Farmer.models import*
from User.models import tbl_booking, tbl_cart
from django.shortcuts import render, get_object_or_404


# Create your views here
def adminregistration(request):
    admin_data = tbl_adminregistration.objects.all()
    if request.method == 'POST':
        name=request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        password=request.POST.get("pswd_password")
        tbl_adminregistration.objects.create(
            adminregistration_name= name,
            adminregistration_email= email,
            adminregistration_password= password
        )
        return redirect("Administrator:AdminRegistration")
    else:
        return render(request,'Administrator/AdminRegistration.html',{"admin":admin_data})
def admindelete(request, id):
    tbl_adminregistration.objects.get(id=id).delete()
    return redirect("Administrator:AdminRegistration")

def editadmin(request,id):
    admin_data = tbl_adminregistration.objects.all()
    editadmin=tbl_adminregistration.objects.get(id=id)
    if request.method=='POST':
        name = request.POST.get("txt_name")
        email=request.POST.get("txt_email")
        password=request.POST.get("pswd_password")
        editadmin.adminregistration_name=name
        editadmin.adminregistration_email=email
        editadmin.adminregistration_password=password
        editadmin.save()
        return redirect("Administrator:AdminRegistration")
    else:
        return render(request,'Administrator/AdminRegistration.html',{'data':editadmin})

def district(request):
    district_data = tbl_district.objects.all()
    if request.method == 'POST':
        district=request.POST.get("txt_district")
        tbl_district.objects.create(
            district_name=district
        )
        return redirect("Administrator:District")
    else:
        return render(request,'Administrator/District.html',{"district": district_data})

def districtdelete(request, id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Administrator:District")
def editdistrict(request,id):
    editdistrict=tbl_district.objects.get(id=id)
    if request.method=='POST':
        name = request.POST.get("txt_district")
        editdistrict.district_name = name
        editdistrict.save()
        return redirect("Administrator:District")
    else:
        return render(request,'Administrator/District.html',{'data':editdistrict})    

def category(request):
    category_data = tbl_category.objects.all()
    if request.method == 'POST':
        category=request.POST.get("txt_category")
        tbl_category.objects.create(
            category_name=category
        )
        return redirect("Administrator:Category")
    else:
        return render(request,'Administrator/Category.html',{'category':category_data})

def categorydelete(request, id):
    tbl_category.objects.get(id=id).delete()
    return redirect("Administrator:Category")
def editcategory(request,id):
    editcategory=tbl_category.objects.get(id=id)
    if request.method=='POST':
        name = request.POST.get("txt_category")
        editcategory.category_name=name
        editcategory.save()
        return redirect("Administrator:Category")
    else:
        return render(request,'Administrator/Category.html',{'data':editcategory})

def place(request):
    district_data = tbl_district.objects.all()
    place_data = tbl_place.objects.all()
    if request.method == 'POST':
        place=request.POST.get("txt_place")
        district_id=request.POST.get("sel_district")
        district_obj=tbl_district.objects.get(id=district_id)
        tbl_place.objects.create(
            place_name = place,
            district = district_obj
        )
        return redirect("Administrator:Place")
    else:
        return render(request,'Administrator/Place.html',{"place":place_data, "district": district_data})
    
def placedelete(request, id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Administrator:Place")
def editplace(request,id):
    district_data = tbl_district.objects.all()
    editplace=tbl_place.objects.get(id=id)
    if request.method=='POST':
        name = request.POST.get("txt_place")
        editplace.place_name = name
        district_id=request.POST.get("sel_district")
        district_obj=tbl_district.objects.get(id=district_id)
        editplace.district=district_obj
        editplace.save()
        return redirect("Administrator:Place")
    else:
        return render(request,'Administrator/Place.html',{'data':editplace, "district": district_data})

def subcategory(request):
    category_data = tbl_category.objects.all()
    subcategory_data = tbl_subcategory.objects.all()
    if request.method == 'POST':
        category=request.POST.get("sel_category")
        subcategory=request.POST.get("txt_subcategory")
        category_obj=tbl_category.objects.get(id=category)
        tbl_subcategory.objects.create(
            category = category_obj,
            subcategory_name = subcategory
        )
        return redirect("Administrator:Subcategory")
    else:
        return render(request,'Administrator/Subcategory.html',{"category": category_data, "subcategory": subcategory_data})

def subcategorydelete(request, id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Administrator:Subcategory")
def editsubcategory(request,id):
    category_data = tbl_category.objects.all()
    editsubcategory=tbl_subcategory.objects.get(id=id)
    if request.method=='POST':
        name = request.POST.get("txt_subcategory")
        editsubcategory.subcategory_name = name
        category_id=request.POST.get("sel_category")
        category_obj=tbl_category.objects.get(id=category_id)
        editsubcategory.category=category_obj
        editsubcategory.save()
        return redirect("Administrator:Subcategory")
    else:
        return render(request,'Administrator/Subcategory.html',{'data':editsubcategory, "category": category_data})

# Administrator/views.py

def HomePage(request):

    # ── Users ──────────────────────────────────────────────────────
    all_users      = tbl_userregistration.objects.all()
    total_users    = all_users.count()
    pending_users  = all_users.filter(user_status=0).count()
    accepted_users = all_users.filter(user_status=1).count()
    rejected_users = all_users.filter(user_status=2).count()

    # ── Catalogue ──────────────────────────────────────────────────
    total_categories    = tbl_category.objects.count()
    total_subcategories = tbl_subcategory.objects.count()
    total_districts     = tbl_district.objects.count()
    total_places        = tbl_place.objects.count()

    # ── Support ────────────────────────────────────────────────────
    total_complaints    = tbl_complaint.objects.count()
    pending_complaints  = tbl_complaint.objects.filter(complaint_status=0).count()
    resolved_complaints = tbl_complaint.objects.filter(complaint_status=1).count()
    total_feedbacks     = tbl_feedback.objects.count()

    # ── Orders ─────────────────────────────────────────────────────
    total_orders     = tbl_booking.objects.count()
    pending_orders   = tbl_cart.objects.filter(cart_status=3).count()
    delivered_orders = tbl_cart.objects.filter(cart_status=6).count()

    
    
    #refunded_orders  = Transaction.objects.filter(
    #                       payment_status__in=['Failed', 'Refunded']
    #                   ).count() 
    
    # ── Revenue ────────────────────────────────────────────────────
    revenue_result = tbl_booking.objects.filter(
                         booking_status =2
                     ).aggregate(total=Sum('booking_amount'))
    total_revenue  = revenue_result['total'] or 0

    # ── Recent rows for tables ────────────────────────────────────
    recent_users        = tbl_userregistration.objects.order_by('-id')[:5]
    recent_complaints   = tbl_complaint.objects.order_by('-id')[:4]
    recent_feedbacks    = tbl_feedback.objects.order_by('-id')[:4]
    recent_orders       = tbl_booking.objects.all().order_by('-id')[:5]
    recent_transactions = tbl_payment.objects.select_related(
    'bookingid__userid'
    ).order_by('-payment_date')[:5]

    context = {
        # users
        'data':             recent_users,       # the template loops over this
        'total_users':      total_users,
        'pending_users':    pending_users,
        'accepted_users':   accepted_users,
        'rejected_users':   rejected_users,

        # catalogue
        'total_categories':    total_categories,
        'total_subcategories': total_subcategories,
        'total_districts':     total_districts,
        'total_places':        total_places,

        # support
        'total_complaints':    total_complaints,
        'pending_complaints':  pending_complaints,
        'resolved_complaints': resolved_complaints,
        'total_feedbacks':     total_feedbacks,

        # orders & payments
        'total_orders':        total_orders,
        'pending_orders':      pending_orders,
        'delivered_orders':    delivered_orders,
        #'refunded_orders':     refunded_orders,
        'total_revenue':       total_revenue,
        

        # recent rows
        'complaint':            recent_complaints,
        'feedback':             recent_feedbacks,
        'recent_orders':        recent_orders,
        'recent_transactions':  recent_transactions,
    }

    return render(request, 'Administrator/Homepage.html', context)

def OrderList(request):
    bookings         = tbl_booking.objects.all().order_by('-id')
    total_orders     = tbl_booking.objects.count()
    placed_orders    = tbl_booking.objects.filter(booking_status=2).count()
    confirmed_orders = tbl_booking.objects.filter(booking_status=3).count()
    shipped_orders   = tbl_booking.objects.filter(booking_status=4).count()
    delivered_orders = tbl_booking.objects.filter(booking_status=6).count()
    cancelled_orders = tbl_booking.objects.filter(booking_status=1).count()

    context = {
        "bookings":         bookings,
        "total_orders":     total_orders,
        "placed_orders":    placed_orders,
        "confirmed_orders": confirmed_orders,
        "shipped_orders":   shipped_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
    }
    return render(request, "Administrator/OrderList.html",context)


def orderdetails(request, id):
    order = get_object_or_404(tbl_booking, id=id)

    order_items = tbl_cart.objects.filter(bookingid=order).select_related(
        'productid', 'productid__category_id', 'productid__farmer_id'
    )

    for item in order_items:
        try:
            price = float(item.productid.product_price)
        except (TypeError, ValueError):
            price = 0
        item.unit_price = price
        item.subtotal = price * item.cart_quantity
    payment = tbl_payment.objects.filter(bookingid=order).order_by('-payment_date').first()

    context = {
        'order': order,
        'order_items': order_items,
        'payment': payment,
    }
    return render(request, 'Administrator/OrderDetails.html', context)

def TransactionList(request):
    revenue_result = tbl_booking.objects.filter(
                         booking_status =2
                     ).aggregate(total=Sum('booking_amount'))
    total_revenue  = revenue_result['total'] or 0

    total_transactions = tbl_payment.objects.count()
    transactions = tbl_payment.objects.all()
    context ={
        'total_revenue':   total_revenue,
        'total_transactions': total_transactions,
        'transactions': transactions,
    }
    return render(request,'Administrator/TransactionList.html',context)

from django.shortcuts import render, get_object_or_404

def transactiondetails(request, id):
    txn = get_object_or_404(tbl_payment, id=id)
    context = {
        'txn': txn,
    }
    return render(request, 'Administrator/TransactionDetails.html', context)

def ExportOrders(request):
    return render (request,'Administrator/ExportOrders.html')

def ExportTransactions(request):
    Complaint=tbl_complaint.objects.all()
    Order = tbl_booking.objects.all()
    Transaction = tbl_cart .objects.all() 
    if request.method == 'GET' and request.GET.get('format'):
        # build and return the file response here
        pass
    context = {
        'total_transactions': Transaction.count(),
        'total_revenue':      Order.filter(booking_status= 2 ).aggregate(Sum('booking_amount'))['booking_amount__sum'] or 0,
        'paid_count':         Transaction.filter(cart_status= 2 ).count(),
        'pending_count':      Transaction.filter(cart_status= 1 ).count(),
        'failed_count':       Transaction.filter(cart_status= 1).count(),
        #'refunded_count':     Transaction.filter(payment_status='Refunded').count(),
        #'recent_exports':     ExportLog.order_by('-created_at')[:5],  # optional model
        'pending_orders':     Transaction.filter(cart_status=1).count(),
        'pending_complaints': Complaint.filter(complaint_status=0).count(),
    }
    return render(request, 'Administrator/ExportTransactions.html', context)

def userlist(request):
    data = tbl_userregistration.objects.all()

    context = {
        'data': data,
        'pending_count': data.filter(user_status=0).count(),
        'accepted_count': data.filter(user_status=1).count(),
        'rejected_count': data.filter(user_status=2).count(),
    }
    return render(request,'Administrator/Userlist.html',context)

def farmerlist(request):
    data = tbl_farmerregistration.objects.all()
    return render(request,'Administrator/Farmerlist.html',{'data': data})

def useraccept(request,uid):
    acc_data = tbl_userregistration.objects.get(id=uid)
    acc_data.user_status = 1
    acc_data.save()
    return render(request,'Administrator/Userlist.html',{'Msg':"Accepted"})

def userrej(request,uid):
    rej_data = tbl_userregistration.objects.get(id=uid)
    rej_data.user_status = 2
    rej_data.save()
    return redirect('Administrator:Userlist',{'Msg':"Rejected"})

def farmerrej(request,uid):
    rej_data = tbl_farmerregistration.objects.get(id=uid)
    rej_data.farmer_status = 2
    rej_data.save()
    return render(request,'Administrator/FarmerList.html',{'Msg':"Rejected"})

def farmeraccept(request,uid):
    acc_data = tbl_farmerregistration.objects.get(id=uid)
    acc_data.farmer_status = 1
    acc_data.save()
    return render(request,'Administrator/FarmerList.html',{'Msg':"Accepted"})


def viewcomplaint(request):
    data=tbl_complaint.objects.all()
    pending_count = data.filter(complaint_status=0).count()  
    replied = data.filter(complaint_status=1).count()      
    return render(request,'Administrator/ViewComplaint.html',{'data':data,'pending_count':pending_count,'replied':replied})

def viewfeedback(request):
    data = tbl_feedback.objects.all()
    unique_users_count = data.values('user_id').distinct().count()
    latest = data.order_by('-feedback_date').first()  # fix 1: use objects.order_by, not tbl_feedback.feedback_date
    latest_submission = latest.feedback_date if latest else None  # fix 2: add = sign, use feedback_date not created_at

    return render(request, 'Administrator/ViewFeedback.html', {
        'data': data,
        'unique_users_count': unique_users_count,  # fix 3: typo was unique_users_coun
        'latest_submission': latest_submission,
    })
def reply(request,uid):
    complaint= tbl_complaint.objects.get(id=uid)
    if request.method=='POST':
        reply=request.POST.get("txt_reply")
        complaint.complaint_reply = reply
        complaint.complaint_status = 1
        complaint.save()
        return redirect('Administrator:ViewComplaint')
    else:
        return render(request,'Administrator/Reply.html',{'data': complaint})

