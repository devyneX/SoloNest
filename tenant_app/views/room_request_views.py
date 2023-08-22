from tenant_app import models, forms
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages



class RoomRequestView(LoginRequiredMixin, CreateView):
    model = models.RoomRequest
    template_name = "tenant_app/room_request.html"
    form_class = forms.RoomRequestForm

    def form_valid(self, form):
        if self.request.user.profile.is_complete():
            form.instance.user = self.request.user
            
            return super().form_valid(form)
        else:
            messages.error(self.request, "Please complete your profile first")
            return redirect("tenant:profile")

    def get_success_url(self):
        return reverse_lazy("tenant:room_request_detail", kwargs={"pk": self.object.pk})


class RoomRequestListView(LoginRequiredMixin, ListView):
    model = models.RoomRequest
    template_name = "tenant_app/room_request_list.html"
    context_object_name = "room_requests"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset.order_by("-date")


class RoomRequestDetailView(LoginRequiredMixin, DetailView):
    model = models.RoomRequest
    template_name = "tenant_app/room_request_detail.html"
    context_object_name = "room_request"

    def get(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().user.pk:
            return redirect("room_request_list")
        return super().get(request, *args, **kwargs)


class RoomRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = models.RoomRequest
    template_name = "tenant_app/room_request.html"
    fields = ["branch", "start_date", "room_type", "ac", "balcony", "attached_bathroom"]
    context_object_name = "room_request"

    def get(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().user.pk:
            return redirect("tenant:room_request_list")
        if self.get_object().status != -1:
            return redirect("tenant:room_request_detail", pk=self.get_object().pk)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().user.pk:
            return redirect("tenant:room_request_list")
        if self.get_object().status != -1:
            return redirect("tenant:room_request_detail", pk=self.get_object().pk)
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("tenant:room_request_detail", kwargs={"pk": self.object.pk})


# class RoomRequestDeleteView(LoginRequiredMixin, DeleteView):
#     model = models.RoomRequest
#     template_name = "tenant_app/room_request_delete.html"
#     context_object_name = "room_request"

#     def get(self, request, *args, **kwargs):
#         if request.user.pk != self.get_object().user.pk:
#             return redirect("tenant:room_request_list")
#         if self.get_object().status != -1:
#             return redirect("tenant:room_request_detail", pk=self.get_object().pk)
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         if request.user.pk != self.get_object().user.pk:
#             return redirect("tenant:room_request_list")
#         if self.get_object().status != -1:
#             return redirect("tenant:room_request_detail", pk=self.get_object().pk)
#         return super().post(request, *args, **kwargs)

#     def get_success_url(self):
#         return reverse_lazy("tenant:room_request_list")
