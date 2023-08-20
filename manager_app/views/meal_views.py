from typing import Any, Dict, Optional
from django.db import models
from django.shortcuts import render
from django.urls import reverse_lazy
from .utils import ManagerRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from manager_app import models
import datetime


class LunchListView(ManagerRequiredMixin, ListView):
    model = models.Meal
    template_name = "manager_app/manager_meal_list.html"
    context_object_name = "meals"

    def get_queryset(self):
        tenants = models.Tenant.objects.filter(room__branch=self.request.user.manager.branch)
        for tenant in tenants:
            if not tenant.is_active():
                continue
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
            if not tenant.is_active():
                continue
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

class MenuMaker(ManagerRequiredMixin, CreateView):
    model = models.MealMonthlyMenu
    template_name = "manager_app/manager_menu_maker.html"
    fields = ["sat_lunch", "sat_dinner", "sun_lunch", "sun_dinner", "mon_lunch", "mon_dinner", "tue_lunch", "tue_dinner", "wed_lunch", "wed_dinner", "thu_lunch", "thu_dinner", "fri_lunch", "fri_dinner"]
    success_url = reverse_lazy("manager:menu")

    def form_valid(self, form):
        form.instance.branch = self.request.user.manager.branch
        return super().form_valid(form)

class MealMenuView(ManagerRequiredMixin, DetailView):
    model = models.MealMonthlyMenu
    template_name = "manager_app/manager_meal_menu.html"
    context_object_name = "menu"

    def get_object(self, queryset=None):
        return models.MealMonthlyMenu.objects.filter(branch=self.request.user.manager.branch).last()

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