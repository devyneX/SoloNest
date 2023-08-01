from django.shortcuts import render
from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class TenantListView(ManagerRequiredMixin, ListView):
    model = models.Tenant
    template_name = "manager_app/manager_tenant_list.html"
    context_object_name = "tenants"


class TenantDetailView(ManagerRequiredMixin, DetailView):
    model = models.Tenant
    template_name = "manager_app/manager_tenant_detail.html"
    context_object_name = "tenant"


# NOTE: not used
class TenantUpdateView(ManagerRequiredMixin, UpdateView):
    model = models.Tenant
    template_name = "manager_app/manager_tenant_update.html"
    context_object_name = "tenant"


# NOTE: might use
class TenantDeleteView(ManagerRequiredMixin, DeleteView):
    model = models.Tenant
    template_name = "manager_app/manager_tenant_delete.html"
    context_object_name = "tenant"
