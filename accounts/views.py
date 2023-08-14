from typing import Optional, Type
from django.forms.forms import BaseForm
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from . import models
from . import forms


# Create your views here.
class UserSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main:home")

        else:
            form = forms.UserSignupForm()
            return render(request, "accounts/signup.html", {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("tenant:profile")

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
                    return redirect("tenant:profile")
                else:
                    return redirect("accounts:login")

            else:
                return render(request, "accounts/signup.html", {"form": form})


class UserUpdateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = forms.UserUpdateForm(instance=request.user)
            return render(request, "accounts/update_user.html", {"form": form})
        else:
            return redirect("accounts:login")

    def post(self, request):
        if request.user.is_authenticated:
            form = forms.UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect("main:home")
            else:
                return render(request, "accounts/update_user.html", {"form": form})
        else:
            return redirect("accounts:login")


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        # TODO: add message to the frontend
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy("admin:index")
        elif self.request.user.is_manager:
            return reverse_lazy("manager:manager_dashboard")
        else:
            return reverse_lazy("tenant:profile")
