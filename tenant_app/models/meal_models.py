from django.db import models
from accounts.models import *
from .room_request_models import Tenant, Branch
from django.utils import timezone


class Meal(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="meals", related_query_name="meal")
    date = models.DateField(default=timezone.now)
    meal_times = [(0, "Lunch"), (1, "Dinner")]
    meal_time = models.SmallIntegerField(choices=meal_times)
    on = models.BooleanField(default=True)
    extra_meal = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    # TODO: add a unique constraint on tenant, date and meal_time

    def get_quantity(self):
        quantity = self.on + self.extra_meal
        return quantity

    def get_price(self):
        self.price = self.get_quantity() * self.tenant.room.branch.meal_price


class MealMonthlyMenu(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="meal_monthly_menus", related_query_name="meal_monthly_menu")
    date = models.DateField(default=timezone.now)
    sat_lunch = models.CharField(max_length=100)
    sat_dinner = models.CharField(max_length=100)
    sun_lunch = models.CharField(max_length=100)
    sun_dinner = models.CharField(max_length=100)
    mon_lunch = models.CharField(max_length=100)
    mon_dinner = models.CharField(max_length=100)
    tue_lunch = models.CharField(max_length=100)
    tue_dinner = models.CharField(max_length=100)
    wed_lunch = models.CharField(max_length=100)
    wed_dinner = models.CharField(max_length=100)
    thu_lunch = models.CharField(max_length=100)
    thu_dinner = models.CharField(max_length=100)
    fri_lunch = models.CharField(max_length=100)
    fri_dinner = models.CharField(max_length=100)
