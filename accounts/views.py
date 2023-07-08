from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import FormView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail

# from .forms import TenantSignUpForm


# Create your views here.


def home(request):
    return render(request, "accounts/home.html")


# class TenantLoginView(FormView):
#     template_name = "accounts/login.html"
#     form_class = TenantLogInForm
#     success_url = "/"

#     def form_valid(self, form):
#         return super().form_valid(form)


class RoomRequestView(CreateView):
    template_name = "accounts/room_request.html"
    form = RoomRequestForm
    model = RoomRequest
    fields = (
        "first_name",
        "last_name",
        "email",
        "single",
        "ac",
        "balcony",
        "attached_bathroom",
    )
    success_url = "/accounts/home"


class TenantSignUpView(View):
    def get(self, request, pk):
        req = RoomRequest.objects.get(pk=pk)
        if req and req.approved:
            form = TenantSignUpForm()
            return render(request, "accounts/signup.html", {"form": form})
        else:
            return render(request, "accounts/room_request.html")

    def post(self, request, pk):
        req = RoomRequest.objects.get(pk=pk)
        if req and req.approved:
            form = TenantSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("home")
            else:
                return render(request, "accounts/signup.html", {"form": form})
        else:
            return render(request, "accounts/room_request.html")


class TenantLoginView(LoginView):
    template_name = "accounts/login.html"
