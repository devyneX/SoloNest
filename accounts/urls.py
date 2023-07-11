from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.UserSignupView.as_view(), name="signup"),
]
