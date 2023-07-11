from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
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
    def get(self, request):
        if request.user.is_authenticated:
            form = forms.UserUpdateForm(instance=request.user)
            return render(request, "accounts/update_user.html", {"form": form})
        else:
            return redirect("login")

    def post(self, request):
        if request.user.is_authenticated:
            form = forms.UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                return render(request, "accounts/update_user.html", {"form": form})
        else:
            return redirect("login")
