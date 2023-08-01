from tenant_app import models
from django.views import View
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


class LaundryRequestView(TenantRequiredMixin, CreateView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request.html"
    # TODO: create a form for this
    fields = ["date"]

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "tenant:laundry_request_detail", kwargs={"pk": self.object.pk}
        )


class LaundryRequestListView(TenantRequiredMixin, ListView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_list.html"
    context_object_name = "laundries"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant=self.request.user.tenant, date__month=datetime.date.today().month
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        return context


class LaundryRequestDetailView(TenantRequiredMixin, DetailView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_detail.html"
    context_object_name = "laundry"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().get(request, *args, **kwargs)


class LaundryRequestUpdateView(TenantRequiredMixin, UpdateView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request.html"
    fields = ["laundry_time", "date"]

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return super().get_success_url()


class LaundryRequestDeleteView(TenantRequiredMixin, DeleteView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_delete.html"
    context_object_name = "laundry"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("tenant:laundry_request_list")


class ReportMissingLaundry(TenantRequiredMixin, View):
    pass


class MissingLaundryListView(TenantRequiredMixin, ListView):
    model = models.LaundryItem
    template_name = "tenant_app/missing_laundry_list.html"
    context_object_name = "laundry_items"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant=self.request.user.tenant, missing=True, found=False
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        return context
