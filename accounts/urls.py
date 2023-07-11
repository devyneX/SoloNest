from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    # path("update-user", views.UserUpdateView.as_view(), name="update_user"),
    # path("change-password", views.UserPasswordChangeView.as_view(), name="change_password"),
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]
