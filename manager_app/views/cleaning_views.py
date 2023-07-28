from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class CleaningRequestListView(ManagerRequiredMixin, ListView):
    model = models.CleaningRequest
    template_name = "manager_app/manager_cleaning_list.html"
    context_object_name = "cleaning_requests"


class CleaningRequestDetailView(ManagerRequiredMixin, DetailView):
    model = models.CleaningRequest
    template_name = "manager_app/manager_cleaning_detail.html"
    context_object_name = "cleaning_request"


class CleaningRequestComplete(ManagerRequiredMixin):
    pass
    # model = models.Cleaning
    # template_name = "manager_app/manager_cleaning_complete.html"
    # context_object_name = "cleaning_request"
    # fields = ["status"]
    # success_url = "/manager/cleaning"
