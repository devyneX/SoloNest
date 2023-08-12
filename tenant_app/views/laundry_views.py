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





# class LaundryRequestView(TenantRequiredMixin, CreateView):
#     model = models.LaundryRequest
#     template_name = "tenant_app/laundry_request.html"
#     form_class = forms.LaundryRequestForm

#     def form_valid(self, form):
#         form.instance.tenant = self.request.user.tenant
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy("tenant:laundry_request_list")


def laundry_request_view(request):
    LaundryItemFormSet = modelformset_factory(models.LaundryItem, form=forms.LaundryItemForm, extra=1, max_num=10)

    if request.method == "POST":
        laundry_request_form = forms.LaundryRequestForm(request.POST)
        laundry_item_formset = LaundryItemFormSet(request.POST, prefix='laundry_item')

        if laundry_request_form.is_valid() and laundry_item_formset.is_valid():
            laundry_request = laundry_request_form.save(commit=False)
            # Set tenant if required, for example:
            laundry_request.tenant = request.user.tenant
            laundry_request.save()
            for item_form in laundry_item_formset:
                item = item_form.save(commit=False)
                item.laundry_request = laundry_request
                item.save()
            return redirect('tenant:laundry_request_list')  # Redirect to a success page
    else:
        laundry_request_form = forms.LaundryRequestForm()
        laundry_item_formset = LaundryItemFormSet(queryset=models.LaundryItem.objects.none(), prefix='laundry_item')

    context = {
        'laundry_request_form': laundry_request_form,
        'laundry_item_formset': laundry_item_formset,
    }

    return render(request, 'tenant_app/laundry_request.html', context)


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
        context["tenant"] = self.request.user.tenant
        return context


class LaundryRequestDetailView(TenantRequiredMixin, DetailView):
    model = models.LaundryRequest
    template_name = "tenant_app/laundry_request_detail.html"
    context_object_name = "laundry"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:laundry_request_list")
        return super().get(request, *args, **kwargs)


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
    pass


class MissingLaundryListView(TenantRequiredMixin, ListView):
    model = models.LaundryItem
    template_name = "tenant_app/missing_laundry_list.html"
    context_object_name = "laundry_items"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant=self.request.user.tenant, missing=True, found=False
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        return context
