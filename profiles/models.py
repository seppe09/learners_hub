from django.db import models
from accounts.models import User
from django.conf import settings

class TeacherProfile(models.Model):
    EDUCATION_LEVEL = [
        ("bachelors", "Bachelors"),
        ("masters", "Masters"),
        ("phd", "PhD"),
    ]
    GENDER = [
        ("male", "Male"),
        ("female", "Female"),
        ("rather not say", "Rather Not Say")
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER, blank=True, null=True)
    profile_image = models.ImageField(upload_to="teacher/profile_images/", blank=True, null=True)
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=10, choices=EDUCATION_LEVEL, default="bachelors")
    expertise = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    languages = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class StudentProfile(models.Model):
    EDUCATION_LEVEL = [
        ("school", "School"),
        ("college", "College"),
        ("working", "Working"),
    ]
    GENDER = [
        ("male", "Male"),
        ("female", "Female"),
        ("rather not say", "Rather Not Say")
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=15, choices=GENDER, blank=True, null=True)
    profile_image = models.ImageField(upload_to="student/profile_images/", blank=True, null=True)  
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=8, choices=EDUCATION_LEVEL, default="school")
    institution = models.CharField(max_length=200, blank=True)
    interests = models.CharField(max_length=200, blank=True)
    goals = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
