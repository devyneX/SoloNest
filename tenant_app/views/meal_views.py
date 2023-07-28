from tenant_app import models
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


class MealRequestView(TenantRequiredMixin, CreateView):
    # TODO: ensure lunch requests cannot be after 11 am and dinner requests cannot be after 5 pm
    model = models.Meal
    template_name = "tenant_app/meal_request.html"
    fields = ["meal_time", "date"]

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("meal_request_detail", kwargs={"pk": self.object.pk})


class MonthlyMealListView(TenantRequiredMixin, ListView):
    model = models.Meal
    template_name = "tenant_app/monthly_meal_list.html"
    context_object_name = "meals"

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


class MealRequestDetailView(TenantRequiredMixin, DetailView):
    model = models.Meal
    template_name = "tenant_app/meal_request_detail.html"
    context_object_name = "meal"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant_monthly_meal_list")
        return super().get(request, *args, **kwargs)


class MealRequestUpdateView(TenantRequiredMixin, UpdateView):
    model = models.Meal
    template_name = "tenant_app/meal_request.html"
    fields = ["meal_time"]
    context_object_name = "meal"

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("meal_request_detail", kwargs={"pk": self.object.pk})


class MealRequestDeleteView(TenantRequiredMixin, DeleteView):
    model = models.Meal
    template_name = "tenant_app/meal_request_delete.html"
    context_object_name = "meal"

    def get_success_url(self):
        return reverse_lazy("tenant:monthly_meal_list")
