from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class CleaningListView(ManagerRequiredMixin, ListView):
    model = models.CleaningRequest
    template_name = "manager_app/manager_cleaning_list.html"
    context_object_name = "cleaning_requests"

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(status=0)

        return queryset.order_by("date", "slot__slot_time")


class CleaningDetailView(ManagerRequiredMixin, DetailView):
    model = models.CleaningRequest
    template_name = "manager_app/manager_cleaning_detail.html"
    context_object_name = "cleaning_request"


class CleaningComplete(ManagerRequiredMixin):
    pass
    # model = models.Cleaning
    # template_name = "manager_app/manager_cleaning_complete.html"
    # context_object_name = "cleaning_request"
    # fields = ["status"]
    # success_url = "/manager/cleaning"
