"""
URL configuration for School_attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls import include


from attendance import views
from School_attendance import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_Login"),
    path('admin_home',views.admin_home,name="admin_home"),
    path('add_staff',views.add_staff,name="add_staff"),
    path('add_staff_save',views.add_staff_save,name="add_staff_save"),
    path('add_student', views.add_student,name="add_student"),
    path('add_student_save', views.add_student_save,name="add_student_save"),
    path('manage_staff', views.manage_staff,name="manage_staff"),
    path('manage_student', views.manage_student,name="manage_student"),
   
    path('edit_staff/<int:teacher_id>/', views.edit_staff,name="edit_staff"),
    path('edit_staff_save', views.edit_staff_save,name="edit_staff_save"),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('delete_student/<int:id>/', views.delete_student, name='delete_student'),
    path('edit_student/<str:student_id>', views.edit_student,name="edit_student"),
    path('edit_student_save', views.edit_student_save,name="edit_student_save"),
    
    path('check_email_exist',views.check_email_exist,name="check_email_exist"),
    path('check_username_exist',views.check_username_exist,name="check_username_exist"),
    path('admin_view_attendance',views.admin_view_attendance,name="admin_view_attendance"),
    path('admin_profile',views.admin_profile,name="admin_profile"),
    path('admin_profile_save',views.admin_profile_save,name="admin_profile_save"),
    path('staff_home', views.staff_home, name="staff_home"),
    path('staff_take_attendance',views.staff_take_attendance,name="staff_take_attendance"),
    path('get_students',views.get_students,name="get_students"),
    path('staff_profile',views.staff_profile,name="staff_profile"),
    path('staff_profile_save',views.staff_profile_save,name="staff_profile_save"),

    path('take_attendance', views.take_attendance, name="take_attendance"),
    path('staff_view_attendance', views.staff_view_attendance, name="staff_view_attendance"),

    path('create_admin_user',views.create_admin_user,name="create_admin_user"),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
