from typing import Any, Dict
from django.shortcuts import render
from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models
import datetime


class LunchListView(ManagerRequiredMixin, ListView):
    model = models.Meal
    template_name = "manager_app/manager_meal_list.html"
    context_object_name = "meals"

    def get_queryset(self):
        tenants = models.Tenant.objects.filter(room__branch=self.request.user.manager.branch)
        for tenant in tenants:
            if not models.Meal.objects.filter(
                tenant=tenant, date=datetime.date.today(), meal_time=0
            ).exists():
                models.Meal.objects.create(
                    tenant=tenant, date=datetime.date.today(), meal_time=0, on=tenant.lunch_default
                )
        queryset = super().get_queryset()
        queryset = queryset.filter(
            on=True,
            meal_time=0,
            date=datetime.date.today(),
            tenant__room__branch=self.request.user.manager.branch,
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meal_time"] = "Lunch"
        return context


class DinnerListView(ManagerRequiredMixin, ListView):
    model = models.Meal
    template_name = "manager_app/manager_meal_list.html"
    context_object_name = "meals"

    def get_queryset(self):
        tenants = models.Tenant.objects.filter(room__branch=self.request.user.manager.branch)
        for tenant in tenants:
            if not models.Meal.objects.filter(
                tenant=tenant, date=datetime.date.today(), meal_time=1
            ).exists():
                models.Meal.objects.create(
                    tenant=tenant, date=datetime.date.today(), meal_time=1, on=tenant.dinner_default
                )

        queryset = super().get_queryset()

        queryset = queryset.filter(
            on=True,
            meal_time=1,
            date=datetime.date.today(),
            tenant__room__branch=self.request.user.manager.branch,
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meal_time"] = "Dinner"
        return context


class MenuMaker(ManagerRequiredMixin):
    pass
