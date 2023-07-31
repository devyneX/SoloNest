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
import datetime


class MealRequestView(TenantRequiredMixin, CreateView):
    model = models.Meal
    template_name = "tenant_app/meal_request.html"
    form_class = forms.MealRequestForm

    def form_valid(self, form):
        # should have only one meal for lunch or dinner on a day
        meal_request = models.Meal.objects.filter(
            tenant=self.request.user.tenant,
            date=form.cleaned_data["date"],
            meal_time=form.cleaned_data["meal_time"],
        )
        if meal_request.exists():
            meal_request[0].update(
                on=form.cleaned_data["on"], extra_meal=form.cleaned_data["extra_meal"]
            )
            return redirect("tenant:meal_request_detail", pk=meal_request.first().pk)

        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tenant:meal_request_detail", kwargs={"pk": self.object.pk})


class MonthlyMealListView(TenantRequiredMixin, ListView):
    model = models.Meal
    template_name = "tenant_app/monthly_meal_list.html"
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
        context["total_lunch"] = queryset.filter(meal_time=0).count()
        context["total_dinner"] = queryset.filter(meal_time=1).count()
        context["total_meal"] = context["total_lunch"] + context["total_dinner"]
        meal_price = self.request.user.tenant.room.branch.meal_price
        context["total_price"] = queryset.aggregate(
            total_price=meal_price * models.Sum(models.F("on") + models.F("extra_meal"))
        )["total_price"]
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
    context_object_name = "meal"

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tenant:meal_request_detail", kwargs={"pk": self.object.pk})


# NOTE: this might not be needed
class MealRequestDeleteView(TenantRequiredMixin, DeleteView):
    model = models.Meal
    template_name = "tenant_app/meal_request_delete.html"
    context_object_name = "meal"

    def get_success_url(self):
        return reverse_lazy("tenant:monthly_meal_list")
