from .utils import ManagerRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.shortcuts import redirect
from manager_app import models


class RepairListView(ManagerRequiredMixin, ListView):
    model = models.RepairRequest
    template_name = "manager_app/manager_repair_list.html"
    context_object_name = "repair_requests"

    def get_queryset(self):
        return super().get_queryset().filter(completed=False).order_by("date")
    
    
# NOTE: this might not be needed
class RepairDetailView(ManagerRequiredMixin, DetailView):
    model = models.RepairRequest
    template_name = "manager_app/manager_repair_detail.html"
    context_object_name = "repair_request"


class RepairComplete(ManagerRequiredMixin, View):
    def get(self, request, pk):
        repair_request = models.RepairRequest.objects.get(pk=pk)
        repair_request.completed = True
        repair_request.save()
        return redirect("manager:repair_list")
    
