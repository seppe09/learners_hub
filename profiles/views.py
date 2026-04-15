from django.shortcuts import render, redirect
from accounts.models import Teacher, Student
from django.contrib.auth.decorators import login_required

@login_required
def create_profile(request):
    if request.method == "POST":
        profile_image = request.FILES.get("profile_image")
        date_of_birth = request.POST.get("date_of_birth") or None
        gender = request.POST.get("gender")
        bio = request.POST.get("bio", "").strip()

        if request.user.is_student and hasattr(request.user, "student"):
            return redirect("profile_page")

        if request.user.is_teacher and hasattr(request.user, "teacher"):
            return redirect("profile_page")

        if request.user.is_teacher:
            qualification = request.POST.get("qualification")
            expertise = request.POST.get("expertise", "").strip()
            experience = request.POST.get("experience")
            languages = request.POST.get("languages", "").strip()

            Teacher.objects.create(
                user=request.user,
                profile_image=profile_image,
                date_of_birth=date_of_birth,
                bio=bio,
                qualification=qualification,
                expertise=expertise,
                experience=experience,
                languages=languages,
            )

        else:
            qualification = request.POST.get("qualification")
            institution = request.POST.get("institution", "").strip()
            interests = request.POST.get("interests", "").strip()
            goals = request.POST.get("goals", "").strip()

            Student.objects.create(
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

        return redirect("dashboard_page")

    return render(request, "profiles/create_profile.html")

@login_required
def view_profile(request):
    user = request.user

    context = {}

    if hasattr(user, "student"):
        context["profile"] = user.student
        context["role"] = "student"

    elif hasattr(user, "teacher"):
        context["profile"] = user.teacher
        context["role"] = "teacher"

    return render(request, "profiles/show_profile.html", context)