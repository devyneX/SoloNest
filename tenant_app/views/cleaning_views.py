from tenant_app import models, forms
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .utils import TenantRequiredMixin
from django.shortcuts import redirect
import datetime


class CleaningRequestView(TenantRequiredMixin, CreateView):
    model = models.CleaningRequest
    template_name = "tenant_app/cleaning_request.html"
    form_class = forms.CleaningRequestForm

    def form_valid(self, form):
        # TODO: ensure only one request per day for the same room
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "tenant:cleaning_request_detail", kwargs={"pk": self.object.pk}
        )


class CleaningRequestListView(TenantRequiredMixin, ListView):
    model = models.CleaningRequest
    template_name = "tenant_app/cleaning_request_list.html"
    context_object_name = "cleaning_requests"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant__room=self.tenant.room, date__month=datetime.date.today().month
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        return context


# NOTE: might not need this view
class CleaningRequestDetailView(TenantRequiredMixin, DetailView):
    model = models.CleaningRequest
    template_name = "tenant_app/cleaning_request_detail.html"
    context_object_name = "cleaning_request"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:cleaning_request_list")
        return super().get(request, *args, **kwargs)


class CleaningRequestUpdateView(TenantRequiredMixin, UpdateView):
    model = models.CleaningRequest
    template_name = "tenant_app/cleaning_request.html"
    fields = ["cleaning_time", "date"]
    context_object_name = "cleaning_request"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:cleaning_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:cleaning_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "tenant:cleaning_request_detail", kwargs={"pk": self.object.pk}
        )


class CleaningRequestDeleteView(TenantRequiredMixin, DeleteView):
    model = models.CleaningRequest
    template_name = "tenant_app/cleaning_request_delete.html"
    context_object_name = "cleaning_request"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:cleaning_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:cleaning_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("tenant:cleaning_request_list")
