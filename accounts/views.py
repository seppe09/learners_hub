from .models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_page")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        role = request.POST.get("role", "")

        form_data = request.POST

        # Validate required fields first
        if not username or not email or not password1 or not role:
            messages.error(request, "All fields are required.")
            return render(request, "accounts/signup.html", {"form_data": form_data})

        if role not in ["teacher", "student"]:
            messages.error(request, "Please select a valid role.")
            return render(request, "accounts/signup.html", {"form_data": form_data})

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "accounts/signup.html", {"form_data": form_data})

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "accounts/signup.html", {"form_data": form_data})

        if User.objects.filter(username=username).exists():
            messages.error(request, "That username is already taken.")
            return render(request, "accounts/signup.html", {"form_data": form_data})

        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with that email already exists.")
            return render(request, "accounts/signup.html", {"form_data": form_data})

        User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        messages.success(request, "Account created! Please sign in.")
        return redirect("login_page")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard_page")

    if request.method == "POST":
        login_input = request.POST.get("login_input", "").strip()
        password = request.POST.get("password", "")

        if not login_input or not password:
            messages.error(request, "Both fields are required.")
            return render(request, "accounts/login.html")

        user = authenticate(request, username=login_input, password=password)

        if user is None and "@" in login_input:
            try:
                matched = User.objects.get(email=login_input.lower())
                user = authenticate(request, username=matched.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "dashboard_page")
            return redirect(next_url)

        messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "accounts/login.html")


@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


def logout_view(request):
    logout(request)
    return redirect("login_page")
