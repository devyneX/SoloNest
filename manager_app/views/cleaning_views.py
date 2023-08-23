from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, FormView
from django.views import View
from django.shortcuts import redirect
from manager_app import models, forms
import datetime

class CleaningListView(ManagerRequiredMixin, ListView):
    model = models.CleaningRequest
    template_name = "manager_app/manager_cleaning_list.html"
    context_object_name = "cleaning_requests"

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(status=0, date=datetime.date.today(), tenant__room__branch=self.request.user.manager.branch)

        return queryset.order_by("slot__time")
    

class CleaningListSearchView(ManagerRequiredMixin, ListView):
    model = models.CleaningRequest
    template_name = "manager_app/manager_cleaning_list.html"
    context_object_name = "cleaning_requests"

    def get_queryset(self):
        queryset = super().get_queryset()

        date = datetime.date(year=self.kwargs["year"], month=self.kwargs["month"], day=self.kwargs["day"])

        queryset = queryset.filter(status=0, date=date, tenant__room__branch=self.request.user.manager.branch)

        return queryset.order_by("slot__time")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date"] = datetime.date(year=self.kwargs["year"], month=self.kwargs["month"], day=self.kwargs["day"])
        return context


class CleaningSearchView(ManagerRequiredMixin, FormView):
    template_name = "manager_app/manager_cleaning_search.html"
    form_class = forms.CleaningSearchForm

    def form_valid(self, form):
        return redirect("manager:cleaning_list_search", year=form.cleaned_data["date"].year, month=form.cleaned_data["date"].month, day=form.cleaned_data["date"].day)


# class CleaningDetailView(ManagerRequiredMixin, DetailView):
#     model = models.CleaningRequest
#     template_name = "manager_app/manager_cleaning_detail.html"
#     context_object_name = "cleaning_request"


class CleaningComplete(ManagerRequiredMixin, View):
    def get(self, request, pk):
        cleaning_request = models.CleaningRequest.objects.get(pk=pk)
        cleaning_request.status = 1
        cleaning_request.save()
        return redirect("manager:cleaning_list")
    

class CleaningIncomplete(ManagerRequiredMixin, View):
    def get(self, request, pk):
        cleaning_request = models.CleaningRequest.objects.get(pk=pk)
        cleaning_request.status = 2
        cleaning_request.save()
        return redirect("manager:cleaning_list")