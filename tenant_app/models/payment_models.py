from django.db import models
from accounts.models import *
from .room_request_models import Tenant, RoomRequest, ArchivedTenant
from django.db.models import F, Sum


class BookingFee(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="booking_fee",
        related_query_name="booking_fee",
    )
    tenant = models.OneToOneField(
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

    amount = models.IntegerField(default=0)
    date = models.DateField(null=True)
    paid = models.BooleanField(default=False)
    method_choices = [(0, "Cash"), (1, "Online")]
    method = models.SmallIntegerField(choices=method_choices, null=True)
    transaction_id = models.CharField(max_length=100, null=True)
    
    archived = models.OneToOneField(ArchivedTenant, on_delete=models.SET_NULL, null=True, related_name="booking_fee", related_query_name="booking_fee")

    def get_amount(self):
        # security deposit is 2 times the rent
        self.amount = 2 * self.room_request.assigned_room.calculate_rent()


class Payment(models.Model):
    tenant = models.OneToOneField(
        Tenant, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="payments", 
        related_query_name="payment"
    )
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
    
    rent = models.IntegerField(default=0)
    meal_due = models.IntegerField(default=0)
    laundry_due = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    date = models.DateField(null=True)
    paid = models.BooleanField(default=False)
    method_choices = [(0, "Cash"), (1, "Online")]
    method = models.SmallIntegerField(choices=method_choices, null=True)
    transaction_id = models.CharField(max_length=100, null=True)

    archived = models.OneToOneField(ArchivedTenant, on_delete=models.SET_NULL, null=True, related_name="payment", related_query_name="payment")

    def get_rent(self):
        self.rent = self.tenant.room.calculate_rent()

    def get_meal_due(self):
        meals = self.tenant.meals.filter(date__month=self.month, date__year=self.year)
        meals_due = meals.filter(on=True).aggregate(total=Sum("price"))["total"]
        self.meal_due = meals_due if meals_due else 0
    
    def get_laundry_due(self):
        laundry_reqs = self.tenant.laundry_requests.filter(
            date__month=self.month, date__year=self.year
        )
        laundry_due = laundry_reqs.filter(status=6).aggregate(
            total=Sum("laundry_item__price")
        )["total"]

        self.laundry_due = laundry_due if laundry_due else 0


    def get_amount(self):
        self.get_rent()
        self.get_meal_due()
        self.get_laundry_due()

        self.amount = self.rent + self.meal_due + self.laundry_due
        
        # TODO: if penalty is added
        # if self.date.day < 5:
        #     return amount
        # elif self.date.day < 10:
        #     return amount + 0.1 * rent
        # elif self.date < 15:
        #     return amount + 0.2 * rent