from tenant_app import models, forms
from django.forms import modelformset_factory
from django.views import View
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
from django.shortcuts import render, redirect
from django.forms import modelformset_factory


class LaundryRequestView(TenantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        LaundryItemFormSet = modelformset_factory(
            models.LaundryItem, form=forms.LaundryItemForm, extra=1, max_num=10
        )
        laundry_request_form = forms.LaundryRequestForm()
        laundry_item_formset = LaundryItemFormSet(
            queryset=models.LaundryItem.objects.none(), prefix="laundry_item"
        )

        context = {
            "laundry_request_form": laundry_request_form,
            "laundry_item_formset": laundry_item_formset,
        }

        return render(request, "tenant_app/laundry_request.html", context)

    def post(self, request, *args, **kwargs):
        LaundryItemFormSet = modelformset_factory(
            models.LaundryItem, form=forms.LaundryItemForm, extra=1, max_num=10
        )

        laundry_request_form = forms.LaundryRequestForm(request.POST)
        laundry_item_formset = LaundryItemFormSet(request.POST, prefix="laundry_item")

        if laundry_request_form.is_valid() and laundry_item_formset.is_valid():
            laundry_request = laundry_request_form.save(commit=False)
            laundry_request.tenant = request.user.tenant
            laundry_request.save()
            for item_form in laundry_item_formset:
                # if form is empty, skip
                if not item_form.cleaned_data:
                    continue
                print(item_form.cleaned_data)
                item = item_form.save(commit=False)
                item.laundry_request = laundry_request
                item.save()
            return redirect("tenant:laundry_request_list")

        context = {
            "laundry_request_form": laundry_request_form,
            "laundry_item_formset": laundry_item_formset,
        }
        return render(request, "tenant_app/laundry_request.html", context)


class LaundryRequestListView(TenantRequiredMixin, ListView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_list.html"
    context_object_name = "laundries"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant=self.request.user.tenant, date__month=datetime.date.today().month
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LaundryRequestDetailView(TenantRequiredMixin, DetailView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_detail.html"
    context_object_name = "laundry"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            # TODO: return Bad Request
            return redirect("tenant:laundry_request_list")
            
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laundry = self.get_object()
        context["laundry_items"] = laundry.laundry_items.all()
        return context


class LaundryRequestUpdateView(TenantRequiredMixin, UpdateView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request.html"
    fields = ["laundry_time", "date"]

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("tenant:laundry_request_list")


class LaundryRequestDeleteView(TenantRequiredMixin, DeleteView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_delete.html"
    context_object_name = "laundry"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("tenant:laundry_request_list")


class ReportMissingLaundry(TenantRequiredMixin, View):
    def get(self, request, pk):
        laundry_item = models.LaundryItem.objects.get(pk=pk)
        if request.user.tenant.pk != laundry_item.laundry_request.tenant.pk:
            return redirect("tenant:laundry_request_list")
        laundry_item.missing = True
        laundry_item.save()
        return redirect("tenant:laundry_request_detail", pk=laundry_item.laundry_request.pk)


class MissingLaundryListView(TenantRequiredMixin, ListView):
    model = models.LaundryItem
    template_name = "tenant_app/missing_laundry_list.html"
    context_object_name = "laundry_items"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            laundry_request__tenant=self.request.user.tenant, missing__in=[1, 2]
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        return context
