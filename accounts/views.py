from django.shortcuts import render
from django.views import View
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import FormView, CreateView
from django.conf import settings
from django.core.mail import send_mail

# from .forms import TenantSignUpForm


# Create your views here.


def test(request):
    return render(request, "accounts/login.html")


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
    success_url = "/"


class TenantSignUp(View):
    def get(self, request, id):
        req = RoomRequest.objects.get(id=id)
        if req and req.approved:
            form = TenantSignUpForm()
            return render(request, "accounts/signup.html", {"form": form})
        else:
            return render(request, "accounts/room_request.html")

    def post(self, request, id):
        req = RoomRequest.objects.get(id=id)
        if req and req.approved:
            form = TenantSignUpForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, "accounts/signup.html", {"form": form})
            else:
                return render(request, "accounts/signup.html", {"form": form})
        else:
            return render(request, "accounts/room_request.html")


# @staff_member_required
# def admin_approval(request, id):
#     req = RoomRequest.objects.filter(id=id)
#     req.approved = True
#     if req:
#         subject = "Welcome to SoloNest"
#         message = f"Hi {req.first_name} {req.second_name}, Your Application has been approved. You have been assigned the room {req.assigned_room}. Please sign up using this link:\n{req.sign_up_link}"
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [
#             req.email,
#         ]
#         send_mail(subject, message, email_from, recipient_list)
#     return render(request, "admin/room_request_change_list.html")
