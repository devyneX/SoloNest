from typing import Any, Optional
from django.db import models
from tenant_app import models, forms
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
from django.db.models import F, Sum, IntegerField
from django.db.models.functions import Cast
import datetime


class MealDefaultView(TenantRequiredMixin, UpdateView):
    model = models.Tenant
    template_name = "tenant_app/meal_default.html"
    fields = ["lunch_default", "dinner_default"]
    success_url = reverse_lazy("tenant:monhtly_meal_list")

    def get_object(self):
        return self.request.user.tenant

class MealRequestView(TenantRequiredMixin, CreateView):
    model = models.Meal
    template_name = "tenant_app/meal_request.html"
    form_class = forms.MealRequestForm
    success_url = reverse_lazy("tenant:monthly_meal_list")

    def form_valid(self, form):
        # should have only one meal for lunch or dinner on a day
        meal_request = models.Meal.objects.filter(
            tenant=self.request.user.tenant,
            date=form.cleaned_data["date"],
            meal_time=form.cleaned_data["meal_time"],
        )
        if meal_request.exists():
            meal_request[0].on = form.cleaned_data["on"]
            meal_request[0].extra_meal = form.cleaned_data["extra_meal"]
            return redirect("tenant:monthly_meal_list")

        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)


class MonthlyMealListView(TenantRequiredMixin, ListView):
    model = models.Meal
    template_name = "tenant_app/meal_request_list.html"
    context_object_name = "meals"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            tenant=self.request.user.tenant, date__month=datetime.date.today().month
        ).order_by("-date", "meal_time")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenant"] = self.request.user.tenant
        queryset = self.get_queryset()
        context["total_lunch"] = (
            queryset.filter(meal_time=0, on=True)
            .annotate(quantity=1 + F("extra_meal"))
            .aggregate(total=Sum("quantity", output_field=IntegerField()))["total"]
        )
        if context["total_lunch"] is None:
            context["total_lunch"] = 0
        context["total_dinner"] = (
            queryset.filter(meal_time=1, on=True)
            .annotate(quantity=1 + F("extra_meal"))
            .aggregate(total=Sum("quantity", output_field=IntegerField()))["total"]
        )
        if context["total_dinner"] is None:
            context["total_dinner"] = 0
        context["total_meal"] = context["total_lunch"] + context["total_dinner"]
        context["meal_price"] = self.request.user.tenant.room.branch.meal_price
        context["total_price"] = context["meal_price"] * context["total_meal"]
        return context


# NOTE: this might not be needed
class MealRequestDetailView(TenantRequiredMixin, DetailView):
    model = models.Meal
    template_name = "tenant_app/meal_request_detail.html"
    context_object_name = "meal"

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:monthly_meal_list")
        return super().get(request, *args, **kwargs)


class MealRequestUpdateView(TenantRequiredMixin, UpdateView):
    model = models.Meal
    template_name = "tenant_app/meal_request.html"
    form_class = forms.MealRequestForm
    success_url = reverse_lazy("tenant:monthly_meal_list")

    def get(self, request, *args, **kwargs):
        if request.user.tenant.pk != self.get_object().tenant.pk:
            return redirect("tenant:monthly_meal_list")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)


# NOTE: this might not be needed
class MealRequestDeleteView(TenantRequiredMixin, DeleteView):
    model = models.Meal
    template_name = "tenant_app/meal_request_delete.html"
    context_object_name = "meal"

    def get_success_url(self):
        return reverse_lazy("tenant:monthly_meal_list")
