from typing import Any, Dict
from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views import View
from django.forms import modelformset_factory
from django.shortcuts import redirect
from manager_app import models, forms



class LaundryListView(ManagerRequiredMixin, ListView):
    model = models.LaundryRequest
    template_name = "manager_app/manager_laundry_list.html"
    context_object_name = "laundry_requests"


    def get_queryset(self):
        d = {k.lower(): v for v, k in models.LaundryRequest.status_choices}
        status = d.get(self.kwargs["status"], None)
        if status is None:
            # TODO: add error handling
            pass

        return models.LaundryRequest.objects.filter(status=status, tenant__room__branch=self.request.user.manager.branch).order_by("date")

    def get_context_data(self):
        LaundrySelectionFormSet = modelformset_factory(models.LaundryRequest, form=forms.LaundrySelectionFrom, extra=0)
        formset = LaundrySelectionFormSet(queryset=self.get_queryset())
        context = {
            "objects_and_forms": zip(self.get_queryset(), formset), 
            "formset": formset,
            "status": self.kwargs["status"],
            }
        return context


class LaundryNextStepView(ManagerRequiredMixin, View):
    def post(self, request, status):
        
        LaundrySelectionFormSet = modelformset_factory(models.LaundryRequest, form=forms.LaundrySelectionFrom, extra=0)
        formset = LaundrySelectionFormSet(request.POST)
        if formset.is_valid():
            next_status = {k.lower(): v for v, k in models.LaundryRequest.status_choices}[status] + 1
            for form in formset:
                if form.cleaned_data["pk"]:
                    form.instance.status = next_status
                    form.save()
        return redirect("manager:laundry_list", status=status)

class LaundryDetailView(ManagerRequiredMixin, DetailView):
    model = models.LaundryRequest
    template_name = "manager_app/manager_laundry_detail.html"
    context_object_name = "laundry_request"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["laundry_items"] = self.get_object().laundry_items.all()
        return context


class LaundryUpdateView(ManagerRequiredMixin, UpdateView):
    model = models.LaundryRequest
    template_name = "manager_app/manager_laundry_update.html"
    context_object_name = "laundry_request"
    fields = ["status"]
    success_url = "/manager/laundry"


class MissingLaundryListView(ManagerRequiredMixin, ListView):
    model = models.LaundryItem
    template_name = "manager_app/manager_missing_laundry.html"
    context_object_name = "laundry_items"

    def get_queryset(self):
        missing = 1 if self.kwargs["missing"] == "missing" else 2
        queryset = super().get_queryset()
        queryset = queryset.filter(missing=missing, laundry_request__tenant__room__branch=self.request.user.manager.branch)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button"] = "Found" if self.kwargs["missing"] == "missing" else "Returned"

        return context

class MissingLaundryUpdateView(ManagerRequiredMixin, View):
    def get(self, request, pk):
        laundry_item = models.LaundryItem.objects.get(pk=pk)
        laundry_item.missing += 1
        laundry_item.save()
        return redirect("manager:missing_laundry_list", "missing")
    