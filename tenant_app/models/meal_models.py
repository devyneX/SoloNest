from django.db import models
from accounts.models import *
from .room_request_models import Tenant
from django.utils import timezone


class Meal(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    meal_times = [(0, "Lunch"), (1, "Dinner")]
    meal_time = models.SmallIntegerField(choices=meal_times)
    on = models.BooleanField(default=True)
    extra_meal = models.IntegerField(default=0)
    # TODO: add a unique constraint on tenant, date and meal_time
    payment = models.ForeignKey("Payment", on_delete=models.CASCADE, null=True)

    def get_quantity(self):
        quantity = self.on + self.extra_meal
        return quantity

    def get_price(self):
        return self.get_quantity() * self.tenant.room.branch.meal_price


class MealMonthlyMenu(models.Model):
    meal_times = [(0, "Lunch"), (1, "Dinner")]
    meal_time = models.SmallIntegerField(choices=meal_times)
    date = models.DateField(default=timezone.now)
    Saturday = models.CharField(max_length=100)
    Sunday = models.CharField(max_length=100)
    Monday = models.CharField(max_length=100)
    Tuesday = models.CharField(max_length=100)
    Wednesday = models.CharField(max_length=100)
    Thursday = models.CharField(max_length=100)
    Friday = models.CharField(max_length=100)
