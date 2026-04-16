from django.urls import path
from profiles.views import create_profile, view_profile, edit_profile

urlpatterns = [
    path("create/", create_profile, name="create_profile_page"),
    path("view/", view_profile, name="view_profile_page"),
    path("edit/", edit_profile, name="edit_profile_page"),
]
