from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class RepairRequestListView(ManagerRequiredMixin, ListView):
    model = models.RepairRequest
    template_name = "manager_app/manager_repair_list.html"
    context_object_name = "repair_requests"


class RepairRequestDetailView(ManagerRequiredMixin, DetailView):
    model = models.RepairRequest
    template_name = "manager_app/manager_repair_detail.html"
    context_object_name = "repair_request"


class RepairRequestComplete(ManagerRequiredMixin):
    pass
