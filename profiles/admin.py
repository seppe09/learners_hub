from django.contrib import admin
from .models import TeacherProfile, StudentProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "qualification", "expertise", "experience"]

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "qualification", "institution"]
