from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile, StudentProfile


@login_required
def create_profile(request):
    # Redirect if profile already exists
    if request.user.has_profile:
        return redirect("view_profile_page")

    if request.method == "POST":
        profile_image = request.FILES.get("profile_image")
        date_of_birth = request.POST.get("date_of_birth") or None
        gender = request.POST.get("gender", "")
        bio = request.POST.get("bio", "").strip()

        if request.user.role == "teacher":
            qualification = request.POST.get("qualification", "bachelors")
            expertise = request.POST.get("expertise", "").strip()
            experience = request.POST.get("experience", 0)
            languages = request.POST.get("languages", "").strip()

            if not expertise or not experience or not languages:
                messages.error(request, "Please fill in all required teacher fields.")
                return render(request, "profiles/create_profile.html")

            TeacherProfile.objects.create(
                user=request.user,
                profile_image=profile_image,
                date_of_birth=date_of_birth,
                gender=gender,
                bio=bio,
                qualification=qualification,
                expertise=expertise,
                experience=experience,
                languages=languages,
            )

        else:
            qualification = request.POST.get("qualification", "school")
            institution = request.POST.get("institution", "").strip()
            interests = request.POST.get("interests", "").strip()
            goals = request.POST.get("goals", "").strip()

            StudentProfile.objects.create(
                user=request.user,
                profile_image=profile_image,
                date_of_birth=date_of_birth,
                gender=gender,
                bio=bio,
                qualification=qualification,
                institution=institution,
                interests=interests,
                goals=goals,
            )

        messages.success(request, "Profile created successfully!")
        return redirect("view_profile_page")

    return render(request, "profiles/create_profile.html")


@login_required
def view_profile(request):
    user = request.user

    if hasattr(user, "student_profile"):
        profile = user.student_profile
        role = "student"
    elif hasattr(user, "teacher_profile"):
        profile = user.teacher_profile
        role = "teacher"
    else:
        return redirect("create_profile_page")

    return render(request, "profiles/view_profile.html", {
        "profile": profile,
        "role": role,
    })


@login_required
def edit_profile(request):
    user = request.user

    if hasattr(user, "student_profile"):
        profile = user.student_profile
        role = "student"
    elif hasattr(user, "teacher_profile"):
        profile = user.teacher_profile
        role = "teacher"
    else:
        return redirect("create_profile_page")

    if request.method == "POST":
        # Update User fields
        user.first_name = request.POST.get("first_name", "").strip()
        user.last_name = request.POST.get("last_name", "").strip()
        new_email = request.POST.get("email", "").strip().lower()

        if new_email and new_email != user.email:
            from accounts.models import User as UserModel
            if UserModel.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, "That email is already in use.")
                return render(request, "profiles/edit_profile.html", {"profile": profile, "role": role})
            user.email = new_email

        # Password change (optional)
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")
        if new_password:
            if len(new_password) < 8:
                messages.error(request, "Password must be at least 8 characters.")
                return render(request, "profiles/edit_profile.html", {"profile": profile, "role": role})
            if new_password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return render(request, "profiles/edit_profile.html", {"profile": profile, "role": role})
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()

        # Update Profile fields
        profile.bio = request.POST.get("bio", "").strip()
        profile.date_of_birth = request.POST.get("date_of_birth") or None
        profile.gender = request.POST.get("gender", "")

        if "profile_image" in request.FILES:
            profile.profile_image = request.FILES["profile_image"]

        if role == "teacher":
            profile.qualification = request.POST.get("qualification", profile.qualification)
            profile.expertise = request.POST.get("expertise", "").strip()
            profile.experience = request.POST.get("experience", profile.experience)
            profile.languages = request.POST.get("languages", "").strip()
        else:
            profile.qualification = request.POST.get("qualification", profile.qualification)
            profile.institution = request.POST.get("institution", "").strip()
            profile.interests = request.POST.get("interests", "").strip()
            profile.goals = request.POST.get("goals", "").strip()

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("view_profile_page")

    return render(request, "profiles/edit_profile.html", {"profile": profile, "role": role})
