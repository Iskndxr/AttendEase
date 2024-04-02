from django.contrib import admin
from .models import CustomUser, Department, Subject, Class, ClassSession, Attendance, MCsubmission, SLsubmission

admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(ClassSession)
admin.site.register(Attendance)
admin.site.register(MCsubmission)
admin.site.register(SLsubmission)
