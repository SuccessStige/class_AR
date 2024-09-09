from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from attendance.models import CustomUser, Student, Attendance, AttendanceReport


# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
