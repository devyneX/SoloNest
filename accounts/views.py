from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# from .forms import TenantSignUpForm


# Create your views here.


def home(request):
    return render(request, "accounts/home.html")


class UserSignupView(View):
    pass


class UserUpdateView(View):
    pass


class UserPasswordChangeView(View):
    pass


class UserLoginView(LoginView):
    pass
    # template_name = "accounts/login.html"
    # redirect_authenticated_user = True

    # def get_success_url(self):
    #     return reverse_lazy("home")
