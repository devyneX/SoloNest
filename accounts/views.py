from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from . import models
from . import forms


# Create your views here.
def home(request):
    return render(request, "accounts/home.html")


class UserSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        else:
            form = forms.UserSignupForm()
            return render(request, "accounts/signup.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        else:
            form = forms.UserSignupForm(request.POST)
            if form.is_valid():
                form.save()
                models.Profile.objects.create(user=form.instance)
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password1"],
                )
                if user is not None:
                    login(request, user)
                    return redirect("home")
                else:
                    return redirect("login")

            else:
                return render(request, "accounts/signup.html", {"form": form})


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
