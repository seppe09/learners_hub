from django.urls import path
from .views import create_profile, view_profile

urlpatterns = [
    path("create_profile/", create_profile, name = "create_profile_page"),
    path("view_profile/", view_profile, name = "view_profile_page"),
]