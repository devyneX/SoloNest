from django.shortcuts import render
from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models
import datetime


class TenantListView(ManagerRequiredMixin, ListView):
    model = models.Tenant
    template_name = "manager_app/manager_tenant_list.html"
    context_object_name = "tenants"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(room__branch=self.request.user.manager.branch)
        return queryset


# class TenantDetailView(ManagerRequiredMixin, DetailView):
#     model = models.Tenant
#     template_name = "manager_app/manager_user_detail.html"
#     context_object_name = "tenant"


class UnpaidListView(ManagerRequiredMixin, ListView):
    model = models.Payment
    template_name = "manager_app/manager_unpaid_list.html"
    context_object_name = "payments"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant__room__branch=self.request.user.manager.branch, paid=False, month=datetime.date.today().month
        )
        return queryset


# NOTE: not used
# class TenantUpdateView(ManagerRequiredMixin, UpdateView):
#     model = models.Tenant
#     template_name = "manager_app/manager_tenant_update.html"
#     context_object_name = "tenant"


# NOTE: might use
# class TenantDeleteView(ManagerRequiredMixin, DeleteView):
#     model = models.Tenant
#     template_name = "manager_app/manager_tenant_delete.html"
#     context_object_name = "tenant"
