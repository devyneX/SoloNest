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


class RepairRequestView(TenantRequiredMixin, CreateView):
    model = models.RepairRequest
    form_class = forms.RepairRequestForm
    template_name = "tenant_app/repair_request.html"

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "tenant:repair_request_list")


class RepairRequestListView(TenantRequiredMixin, ListView):
    model = models.RepairRequest
    template_name = "tenant_app/repair_request_list.html"
    context_object_name = "repairs"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tenant=self.request.user.tenant).order_by("-date")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        return context


# class RepairRequestDetailView(TenantRequiredMixin, DetailView):
#     model = models.RepairRequest
#     template_name = "tenant_app/repair_request_list.html"
#     context_object_name = "repair"

#     def get(self, request, *args, **kwargs):
#         if request.user.tenant.pk != self.get_object().tenant.pk:
#             return redirect("tenant:repair_request_list")
#         return super().get(request, *args, **kwargs)


class RepairRequestUpdateView(TenantRequiredMixin, UpdateView):
    model = models.RepairRequest
    form_class = forms.RepairRequestForm
    template_name = "tenant_app/repair_request.html"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:repair_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:repair_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "tenant:repair_request_list"
        )


# class RepairRequestDeleteView(TenantRequiredMixin, DeleteView):
#     model = models.RepairRequest
#     form_class = forms.RepairRequestForm
#     template_name = "tenant_app/repair_request_delete.html"
#     context_object_name = "repair"

#     def get(self, request, *args, **kwargs):
#         if request.user.tenant.pk != self.get_object().tenant.pk:
#             return redirect("tenant:repair_request_list")
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         if request.user.tenant.pk != self.get_object().tenant.pk:
#             return redirect("tenant:repair_request_list")
#         return super().post(request, *args, **kwargs)

#     def get_success_url(self):
#         return reverse_lazy("tenant:repair_request_list")
