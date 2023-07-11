from django.shortcuts import render, redirect
from django.views import View

from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms


# Create your views here.
class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        return render(
            request, "room_management/profile.html", {"profile": user.profile}
        )


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = forms.ProfileUpdateForm(instance=user.profile)
        return render(request, "room_management/profile_update.html", {"form": form})

    def post(self, request):
        user = request.user
        form = forms.ProfileUpdateForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "room_management/profile_update.html", {"form": form})


class RoomRequestView(LoginRequiredMixin, CreateView):
    model = models.RoomRequest
    template_name = "room_management/room_request.html"
    fields = ["room_type", "ac", "balcony", "attached_bathroom"]

    def form_valid(self, form):
        if self.request.user.profile.is_complete():
            print("here")
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            print("here")
            return redirect("room_request")

    def get_success_url(self):
        return reverse_lazy("room_request_detail", kwargs={"pk": self.object.pk})


class RoomRequestListView(LoginRequiredMixin, ListView):
    model = models.RoomRequest
    template_name = "room_management/room_request_list.html"
    context_object_name = "room_requests"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class RoomRequestDetailView(LoginRequiredMixin, DetailView):
    model = models.RoomRequest
    template_name = "room_management/room_request_detail.html"
    exclude = ["user", "status", "assigned_room"]
    context_object_name = "room_request"

    def get(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().user.pk:
            return redirect("room_request_list")
        return super().get(request, *args, **kwargs)


class RoomRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = models.RoomRequest
    template_name = "room_management/room_request.html"
    fields = ["room_type", "ac", "balcony", "attached_bathroom"]
    context_object_name = "room_request"

    def form_valid(self, form):
        if self.request.user.pk != form.instance.user.pk:
            return redirect("room_request_list")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("room_request_detail", kwargs={"pk": self.object.pk})


class RoomRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = models.RoomRequest
    template_name = "room_management/room_request_delete.html"
    context_object_name = "room_request"

    def form_valid(self, form):
        if self.request.user.pk != self.get_object().user.pk:
            return redirect("room_request_list")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("room_request_list")
