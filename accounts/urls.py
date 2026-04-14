from django.urls import path
from .views import signup_view, login_view, dashboard_view, logout_view

urlpatterns = [
    path('signup/', signup_view, name="signup_page"),
    path('login/', login_view, name="login_page"),
    path('dashboard/', dashboard_view, name="dashboard_page"),
    path('logout/', logout_view, name="logout_page"),
]