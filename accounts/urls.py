from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.urls import reverse_lazy

app_name = "accounts"

urlpatterns = [
    path("signup/", views.UserSignupView.as_view(), name="signup"),
    path("update-user/", views.UserUpdateView.as_view(), name="update_user"),
    path(
        "change-password/",
        PasswordChangeView.as_view(
            template_name="accounts/paasword_change.html",
            success_url=reverse_lazy("accounts:login"),
        ),
        name="change_password",
    ),
    path(
        "login/",
        views.UserLoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
]
