from django.shortcuts import render
from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class MealListView(ManagerRequiredMixin, ListView):
    model = models.Meal
    template_name = "manager_app/manager_meal_list.html"
    context_object_name = "meals"


class MenuMaker(ManagerRequiredMixin):
    pass
