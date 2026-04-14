from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class Teacher(models.Model):
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to="teacher/profile_images/", blank=True, null=True)
    gender = models.CharField(max_length=15, choices=GENDER, blank=True, null=True)
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=10, choices=EDUCATION_LEVEL, default="bachelors")
    expertise = models.CharField(max_length=200)
    experience = models.PositiveIntegerField()
    languages = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
class Student(models.Model):
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=15, choices=GENDER, blank=True, null=True)
    profile_image = models.ImageField(upload_to="student/profile_images/", blank=True, null=True)  
    bio = models.TextField(blank=True)
    qualification = models.CharField(max_length=8, choices=EDUCATION_LEVEL, default="school")
    institution = models.CharField(max_length=200)
    interests = models.CharField(max_length=200)
    goals = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
        
