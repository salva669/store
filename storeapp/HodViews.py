from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from storeapp.models import CustomUser, Staffs, Stocks, Subjects, FeedBackStaffs,  LeaveReportStaff

def admin_home(request):
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    stock_count=Stocks.objects.all().count()

    stock_all=Stocks.objects.all()
    stock_name_list=[]
    subject_count_list=[]
    student_count_list_in_stock=[]
    for stock in stock_all:
        subjects=Subjects.objects.filter(stock_id=stock.id).count()
        
        stock_name_list.append(stock.stock_name)
        subject_count_list.append(subjects)
        

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        stock=Stocks.objects.get(id=subject.stock_id.id)
        
        subject_list.append(subject.subject_name)
        

    staffs=Staffs.objects.all()
    staff_name_list=[]
    for staff in staffs:
        subject_ids=Subjects.objects.filter(staff_id=staff.admin.id)
        leaves=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
        staff_name_list.append(staff.admin.username)

   


    return render(request,"boss_template/home_content.html",{"staff_count":staff_count,"subject_count":subject_count,"stock_count":stock_count,"stock_name_list":stock_name_list,"subject_count_list":subject_count_list, "subject_list":subject_list,"staff_name_list":staff_name_list})

def add_staff(request):
    return render(request,"boss_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_stock(request):
    return render(request,"boss_template/add_stock_template.html")

def add_stock_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        stock=request.POST.get("stock")
        try:
            stock_model=Stocks(stock_name=stock)
            stock_model.save()
            messages.success(request,"Successfully Added Stock")
            return HttpResponseRedirect(reverse("add_stock"))
        except:
            messages.error(request,"Failed To Add Stock")
            return HttpResponseRedirect(reverse("add_stock"))

def add_subject(request):
    stocks=Stocks.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"boss_template/add_subject_template.html",{"staffs":staffs,"stocks":stocks})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        stock_id=request.POST.get("stock")
        stock=Stocks.objects.get(id=stock_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,stock_id=stock,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"boss_template/manage_staff_template.html",{"staffs":staffs})

def manage_stock(request):
    stocks=Stocks.objects.all()
    return render(request,"boss_template/manage_stock_template.html",{"stocks":stocks})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"boss_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"boss_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    stocks=Stocks.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"boss_template/edit_subject_template.html",{"subject":subject,"staffs":staffs,"stocks":stocks,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        stock_id=request.POST.get("stock")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            stock=Stocks.objects.get(id=stock_id)
            subject.stock_id=stock
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))


def edit_stock(request,stock_id):
    stock=Stocks.objects.get(id=stock_id)
    return render(request,"boss_template/edit_stock_template.html",{"stock":stock,"id":stock_id})

def edit_stock_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        stock_id=request.POST.get("stock_id")
        stock_name=request.POST.get("stock")
        try:
            stock=Stocks.objects.get(id=stock_id)
            stock.stock_name=stock_name
            stock.save()
            messages.success(request,"Successfully Edited Stock")
            return HttpResponseRedirect(reverse("edit_stock",kwargs={"stock_id":stock_id}))
        except:
            messages.error(request,"Failed to Edit Stock")
            return HttpResponseRedirect(reverse("edit_stock",kwargs={"stock_id":stock_id}))

def staff_feedback_message(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"boss_template/staff_feedback_template.html",{"feedbacks":feedbacks})

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"boss_template/staff_leave_view.html",{"leaves":leaves})

def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))

def admin_send_notification_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"boss_template/staff_notification.html",{"staffs":staffs})

@csrf_exempt
def send_staff_notification(request):
    id=request.POST.get("id")
    message=request.POST.get("message")
    staff=Staffs.objects.get(admin=id)
    token=staff.fcm_token
    url="https://fcm.googleapis.com/fcm/send"
    body={
        "notification":{
            "title":"Student Management System",
            "body":message,
            "click_action":"https://studentmanagementsystem22.herokuapp.com/staff_all_notification",
            "icon":"http://studentmanagementsystem22.herokuapp.com/static/dist/img/user2-160x160.jpg"
        },
        "to":token
    }
    headers={"Content-Type":"application/json","Authorization":"key=SERVER_KEY_HERE"}
    data=requests.post(url,data=json.dumps(body),headers=headers)
    notification=NotificationStaffs(staff_id=staff,message=message)
    notification.save()
    print(data.text)
    return HttpResponse("True")

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"boss_template/admin_profile.html",{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

@csrf_exempt
def check_email_exist(request):
    email=request.POST.get("email")
    user_obj=CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username=request.POST.get("username")
    user_obj=CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
