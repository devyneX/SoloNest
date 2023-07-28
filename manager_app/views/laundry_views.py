from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class LaundryRequestListView(ManagerRequiredMixin, ListView):
    model = models.LaundryRequest
    template_name = "manager_app/manager_laundry_list.html"
    context_object_name = "laundry_requests"


class LaundryRequestDetailView(ManagerRequiredMixin, DetailView):
    model = models.LaundryRequest
    template_name = "manager_app/manager_laundry_detail.html"
    context_object_name = "laundry_request"


class LaundryRequestUpdateView(ManagerRequiredMixin, UpdateView):
    model = models.LaundryRequest
    template_name = "manager_app/manager_laundry_update.html"
    context_object_name = "laundry_request"
    fields = ["status"]
    success_url = "/manager/laundry"


class MissingLaundryListView(ManagerRequiredMixin, ListView):
    model = models.LaundryItem
    template_name = "manager_app/manager_missing_laundry_list.html"
    context_object_name = "missing_laundry_requests"


class MissingLaundryFoundView(ManagerRequiredMixin):
    pass
