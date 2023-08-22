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
    success_url = reverse_lazy("tenant:monthly_meal_list")

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
            meal_request = meal_request.first()
            meal_request.on = form.cleaned_data["on"]
            meal_request.extra_meal = form.cleaned_data["extra_meal"]
            meal_request.price = self.request.user.tenant.room.branch.meal_price * form.instance.get_quantity()
            meal_request.save()
            return redirect("tenant:monthly_meal_list")

        form.instance.tenant = self.request.user.tenant
        form.instance.price = self.request.user.tenant.room.branch.meal_price * form.instance.get_quantity()
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
        context["total_price"] = queryset.aggregate(price=Sum("price"))["price"]
        return context


# NOTE: this might not be needed
# class MealRequestDetailView(TenantRequiredMixin, DetailView):
#     model = models.Meal
#     template_name = "tenant_app/meal_request_detail.html"
#     context_object_name = "meal"

#     def get(self, request, *args, **kwargs):
#         if request.user.tenant.pk != self.get_object().tenant.pk:
#             return redirect("tenant:monthly_meal_list")
#         return super().get(request, *args, **kwargs)


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
        form.instance.price = self.request.user.tenant.room.branch.meal_price * form.instance.get_quantity()
        return super().form_valid(form)


# NOTE: this might not be needed
# class MealRequestDeleteView(TenantRequiredMixin, DeleteView):
#     model = models.Meal
#     template_name = "tenant_app/meal_request_delete.html"
#     context_object_name = "meal"

#     def get_success_url(self):
#         return reverse_lazy("tenant:monthly_meal_list")


class MenuView(TenantRequiredMixin, DetailView):
    model = models.MealMonthlyMenu
    template_name = "tenant_app/meal_menu.html"
    context_object_name = "menu"

    def get_object(self, queryset=None):
        return models.MealMonthlyMenu.objects.filter(branch=self.request.user.tenant.room.branch).last()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = self.get_object()
        if menu is None:
            return context
        
        context["meals"] = [
            ("Saturday", menu.sat_lunch, menu.sat_dinner), 
            ("Sunday", menu.sun_lunch, menu.sun_dinner), 
            ("Monday", menu.mon_lunch, menu.mon_dinner), 
            ("Tuesday", menu.tue_lunch, menu.tue_dinner), 
            ("Wednesday", menu.wed_lunch, menu.wed_dinner), 
            ("Thursday", menu.thu_lunch, menu.thu_dinner), 
            ("Friday", menu.fri_lunch, menu.fri_dinner)
        ]

        return context