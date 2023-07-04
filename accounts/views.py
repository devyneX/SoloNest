from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .models import *
from .forms import *
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout

# from .forms import TenantSignUpForm


# Create your views here.


def test(request):
    return render(request, "accounts/login.html")


# class TenantSignUp(FormView):
#     template_name = "accounts/tenant_signup.html"
#     form_class = TenantSignUpForm

#     def get_success_url(self):
#         return reverse("tenant_login")

#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
