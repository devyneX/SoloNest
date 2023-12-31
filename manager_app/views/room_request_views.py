from .utils import ManagerRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from manager_app import models, forms
import datetime


class RoomRequestListView(ManagerRequiredMixin, ListView):
    model = models.RoomRequest
    template_name = "manager_app/manager_room_request_list.html"
    context_object_name = "room_requests"
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(
            branch=self.request.user.manager.branch, status=-1
        ).order_by("start_date", "date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_requests = context["room_requests"]
        context["room_requests"] = []
        for room_request in room_requests:
            context["room_requests"].append(
                (room_request, room_request.get_available_rooms().count())
            )
        return context


class RoomRequestDetailView(ManagerRequiredMixin, DetailView):
    model = models.RoomRequest
    template_name = "manager_app/manager_room_request_detail.html"
    context_object_name = "room_request"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["no_of_available_rooms"] = (
            context["room_request"].get_available_rooms().count()
        )
        return context


class RoomRequestApprovalView(ManagerRequiredMixin, UpdateView):
    model = models.RoomRequest
    form_class = forms.RoomRequestApprovalForm
    template_name = "manager_app/manager_room_request_approval.html"
    success_url = reverse_lazy("manager:room_request_list")

    def form_valid(self, form):
        form.instance.status = 1
        form.instance.assigned_room = form.cleaned_data["assigned_room"]
        form.instance.expiry_date = datetime.datetime.now() + datetime.timedelta(days=3)

        booking_fee = models.BookingFee.objects.create(
            room_request=form.instance,
            user=form.instance.user,
        )

        booking_fee.get_amount()
        booking_fee.save()

        subject = "Room Request Approved"
        message = f"Your room request has been approved. You have been assigned room no. {form.instance.assigned_room.room_no}. Please pay the booking fee of TK. {booking_fee.amount} to confirm your booking."
        from_email = settings.EMAIL_HOST_USER
        recepient_list = [form.instance.user.email]
        send_mail(subject, message, from_email, recepient_list)
        return super().form_valid(form)


class RoomRequestRejectionView(ManagerRequiredMixin, UpdateView):
    model = models.RoomRequest
    form_class = forms.RoomRequestRejectionForm
    template_name = "manager_app/manager_room_request_rejection.html"
    success_url = reverse_lazy("manager:room_request_list")

    def form_valid(self, form):
        form.instance.status = 0
        return super().form_valid(form)
