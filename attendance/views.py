from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, User
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from attendance.form import AttendanceForm
from django.utils import timezone
from django.db.models import Count, Q
from datetime import date

from attendance.form import AddStudentForm,EditStudentForm
from attendance.models import CustomUser, Teacher, Student,Attendance,AttendanceReport
from attendance.EmailBackEnd import EmailBackEnd

# Create your views here.
def showDemoPage(request):
    return render(request,"demo.html")

# Functions that show Login page
def ShowLoginPage(request):
    return render(request,"login_page.html")
# Login Function 
def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type =="1":
                return HttpResponseRedirect('/admin_home')
            else:
                return HttpResponseRedirect(reverse("staff_home"))
            
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")
            # messages.error(request,"Invalid Login Details")
            # return HttpResponseRedirect("/")
def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")
# Logout FUnction 
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

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
            user.teacher.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        
def manage_staff(request):
    teachers=Teacher.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"teachers":teachers})
# View to render the edit form

def edit_staff(request, teacher_id):
    try:
        # Get the CustomUser instance by ID
        admin = get_object_or_404(CustomUser, id=teacher_id)

        # Get the Teacher instance associated with this CustomUser
        teacher = get_object_or_404(Teacher, admin=admin)

        return render(request, "hod_template/edit_staff_template.html", {"teacher": teacher, "id": teacher_id})
    
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher not found")
        return redirect("manage_staff")  # Redirect if no Teacher is found

def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        teacher_id = request.POST.get("teacher_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            # Get the CustomUser instance by ID
            admin = get_object_or_404(CustomUser, id=teacher_id)

            # Ensure the Teacher instance exists
            teacher = Teacher.objects.filter(admin=admin).first()
            if not teacher:
                raise Exception("No Teacher matches the given query.")

            # Update user details
            admin.first_name = first_name
            admin.last_name = last_name
            admin.email = email
            admin.username = username
            admin.save()

            # Update teacher details
            teacher.address = address
            teacher.save()

            # Check if the user with id 1 is linked to a teacher
            admin = CustomUser.objects.get(id=1)
            teacher = Teacher.objects.filter(admin=admin).exists()
            print(teacher)  # This should return True if a Teacher is linked


            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"teacher_id": teacher_id}))
        except Exception as e:
            messages.error(request, f"Failed to Edit Staff: {e}")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"teacher_id": teacher_id}))

def edit_student(request,student_id):
    request.session['student_id']=student_id
    student=Student.objects.get(admin=student_id)
    form=EditStudentForm()
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['date_of_birth'].initial=student.date_of_birth
    form.fields['address'].initial=student.address
    form.fields['sex'].initial=student.gender
    return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id=request.session.get("student_id")
        if student_id==None:
            return HttpResponseRedirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            date_of_birth = form.cleaned_data["date_of_birth"]
            sex = form.cleaned_data["sex"]

            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Student.objects.get(admin=student_id)
                student.address=address
                student.gender=sex
                student.date_of_birth=date_of_birth
                student.save()
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Student.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})



def add_student(request):
    form=AddStudentForm()
    return render(request,"hod_template/add_student_template.html",{"form":form})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            gender = form.cleaned_data["sex"]
            date_of_birth = form.cleaned_data.get("date_of_birth")

            try:
                # Create a CustomUser instance with user_type 3 (Student)
                user = CustomUser.objects.create_user(
                    username=username, 
                    password=password, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name, 
                    user_type=3
                )
                user.save()

                # Create a Student instance linked to the CustomUser instance
                student = Student.objects.create(
                    admin=user,  # Correctly linking the Student to CustomUser
                    address=address,
                    gender=gender,
                    date_of_birth=date_of_birth,
                )
                student.save()

                messages.success(request, "Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except:
                messages.error(request, "Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            return render(request, "hod_template/add_student_template.html", {"form": form})


def manage_student(request):
    students = Student.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students": students})

def admin_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    return render(request,"hod_template/admin_profile.html",{"user":user})

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
            messages.success(request, "Successfully Uploaded a Profil")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Uploaded a Profil")
            return HttpResponseRedirect(reverse("admin_profile"))


def delete_teacher(request,teacher_id):
    teacher = Teacher.objects.get(admin=teacher_id)
    teacher.delete()
    return HttpResponse("Successfully Deleted")

def delete_student(request,id):
    students = Student.objects.get(admin=id)
    students.delete()
    return HttpResponse("Successfully Deleted")

# Check if Email and Username Exist

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
    
def admin_view_attendance(request):
    students = Student.objects.all()
    attendance_reports = AttendanceReport.objects.select_related('attendance__student_id').all()
    return render(request, 'hod_template/admin_view_attendance.html', {'students': students,'attendance_reports': attendance_reports})

def staff_view_attendance(request):
    students = Student.objects.all()
    attendance_reports = AttendanceReport.objects.select_related('attendance__student_id').all()
    return render(request, 'hod_template/admin_view_attendance.html', {'students': students,'attendance_reports': attendance_reports})


def staff_home(request):
    return render(request,"staff_template/staff_home_template.html")



def take_attendance(request):
    if request.method == 'POST':
        students = Student.objects.all()
        attendance=Attendance.objects.all()

        for student in students:
            status = request.POST.get(f'status_{student.id}')
            attendance_date = timezone.now().date()

            if not status:
                messages.error(request, f"Please mark attendance for {student.admin.first_name} {student.admin.last_name}.")
                return redirect('take_attendance')

            # Create or update the attendance entry
            attendance, created = Attendance.objects.get_or_create(student_id=student, attendance_date=attendance_date)
            AttendanceReport.objects.update_or_create(attendance=attendance, defaults={'status': status})

        messages.success(request, "Attendance marked successfully")
        return redirect('staff_take_attendance')

    else:
        students = Student.objects.all()
        attendance_date = timezone.now().date()
        return render(request, 'staff_template/staff_take_attendance.html', {'students': students, 'attendance_date': attendance_date})



def staff_take_attendance(request):
    students=Student.objects.all()
    return render(request,"staff_template/staff_take_attendance.html",{"students":students})
   
@csrf_exempt
def get_students(request):
    students = Student.objects.all()
    return render(request, 'staff_template/staff_take_attendance.html', {'students': students})


def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Student.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"student":student})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Uploaded a Profil")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Uploaded a Profil")
            return HttpResponseRedirect(reverse("staff_profile"))

# def attendance_summary(request):
#     total_students=Student.objects.count()
#     total_teachers=Teacher.objects.count()
#     total_present=AttendanceReport.objects.filter(status='Present').count()
#     total_absent=AttendanceReport.objects.filter(status='Absent').count()
    
#     return render(request, "hod_template/home_content.html", {"total_students": total_students,"total_teachers": total_teachers,"total_present": total_present,"total_absent": total_absent})
def admin_home(request):
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    total_present = AttendanceReport.objects.filter(status='Present').count()
    total_absent = AttendanceReport.objects.filter(status='Absent').count()

    return render(request,"hod_template/home_content.html",{
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_present": total_present,
        "total_absent": total_absent
    })

def staff_home(request):
    total_teachers = Teacher.objects.count()
    total_students = Student.objects.count()
    total_present = AttendanceReport.objects.filter(status='Present').count()
    total_absent = AttendanceReport.objects.filter(status='Absent').count()

    return render(request,"staff_template/staff_home_template.html",{
        "total_teachers": total_teachers,
        "total_students": total_students,
        "total_present": total_present,
        "total_absent": total_absent
    })

def create_admin_user(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
        return HttpResponse("Superuser created successfully!")
    else:
        return HttpResponse("Superuser already exists.")