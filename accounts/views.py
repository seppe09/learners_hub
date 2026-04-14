from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("signup_page")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect("signup_page")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("signup_page")

        if role == "teacher":
            is_teacher = True
            is_student = False
        else:
            is_teacher = False
            is_student = True

        if role not in ["teacher", "student"]:
            messages.error(request, "Invalid role selected")
            return redirect("signup_page")
        
        if not username or not email or not password1:
            messages.error(request, "All fields are required")
            return redirect("signup_page")

        User.objects.create_user(
            username = username,
            email = email,
            password = password1,
            first_name = first_name,
            last_name = last_name,
            is_teacher = is_teacher,
            is_student = is_student,
        )
        return redirect('login_page')
    
    return render(request, "accounts/signup.html")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_page")
    
    if request.method == "POST":
        login_input = request.POST.get("login_input", "").strip()
        password = request.POST.get("password")
        
        print(login_input)
        print(password)
        
        if not login_input or not password:
            messages.error(request, "All fields are required.")
            return redirect("login_page")
        
        user = authenticate(request, username = login_input, password = password)
        
        if user is None and "@" in login_input:
            try:
                user_email = User.objects.get(email = login_input)
                user = authenticate(request, username = user_email.username, password = password)
                
            except User.DoesNotExist:
                pass
            
        if user is not None:
            login(request, user)
            return redirect("dashboard_page")
        
        if "@" in login_input:
            messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid username or password")               
        
    return render(request, "accounts/login.html")

@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")

def logout_view(request):
    logout(request)
    return redirect("login_page")
