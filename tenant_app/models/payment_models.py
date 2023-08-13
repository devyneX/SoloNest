from django.db import models
from accounts.models import *
from .room_request_models import Tenant, RoomRequest
from django.utils import timezone
from django.db.models import F, Sum


class BookingFee(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="booking_fee",
        related_query_name="booking_fee",
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        related_name="booking_fee",
        related_query_name="booking_fee",
    )
    room_request = models.OneToOneField(
        RoomRequest,
        on_delete=models.SET_NULL,
        null=True,
        related_name="booking_fee",
        related_query_name="booking_fee",
    )
    date = models.DateField(null=True)
    paid = models.BooleanField(default=False)
    method_choices = [(0, "Cash"), (1, "Online")]
    method = models.SmallIntegerField(choices=method_choices, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def get_amount(self):
        # security deposit is 2 times the rent
        amount = 2 * self.room_request.assigned_room.calculate_rent()
        return amount


class Payment(models.Model):
    tenant = models.ForeignKey(
        Tenant, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="payments", 
        related_query_name="payment"
    )
    date = models.DateField(null=True)
    month_choices = [
        (1, "January"),
        (2, "February"),
        (3, "March"),
        (4, "April"),
        (5, "May"),
        (6, "June"),
        (7, "July"),
        (8, "August"),
        (9, "September"),
        (10, "October"),
        (11, "November"),
        (12, "December"),
    ]
    month = models.SmallIntegerField(choices=month_choices)
    year = models.SmallIntegerField()
    paid = models.BooleanField(default=False)
    method_choices = [(0, "Cash"), (1, "Online")]
    method = models.SmallIntegerField(choices=method_choices, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def get_amount(self):
        rent = self.tenant.room.rent
        meals = self.tenant.meals.filter(date__month=self.month, date__year=self.year)
        meals_due = (
            self.tenant.room.branch.meal_price
            * meals.filter(on=True)
            .annotate(quantity=1 + F("extra_meals"))
            .aggregate(total=Sum("quantity"))["total"]
        )
        laundry_reqs = self.tenant.laundry.filter(
            date__month=self.month, date__year=self.year
        )
        laundry_due = laundry_reqs.filter(status=6).aggregate(
            total=Sum("laundry_items__price")
        )["total"]

        amount = rent + meals_due + laundry_due

        # if self.date.day < 5:
        #     return amount
        # elif self.date.day < 10:
        #     return amount + 0.1 * rent
        # elif self.date < 15:
        #     return amount + 0.2 * rent

        return amount
