from django.db import models
from .room_request_models import Tenant
from django.utils import timezone


class LaundryRequest(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="laundry_requests",
        related_query_name="laundry_request",
    )
    date = models.DateField(default=timezone.now)
    status_choices = [
        (0, "Pending"),
        (1, "Received"),
        (2, "Washing"),
        (3, "Drying"),
        (4, "Ironing"),
        (5, "Ready"),
        (6, "Delivered"),
    ]
    status = models.SmallIntegerField(choices=status_choices, default=0)

    def calculate_price(self):
        price = 0
        for item in self.laundry_items.all():
            price += item.calculate_price()
        return price


class LaundryItem(models.Model):
    laundry_request = models.ForeignKey(
        LaundryRequest,
        on_delete=models.CASCADE,
        related_name="laundry_items",
        related_query_name="laundry_item",
    )
    item_choices = [
        ("shirt", "Shirt"),
        ("pant", "Pant"),
        ("t-shirt", "T-Shirt"),
        ("sweater", "Sweater"),
        ("blanket", "Blanket"),
        ("bedsheet", "Bedsheet"),
        ("pillow cover", "Pillow Cover"),
    ]
    item = models.CharField(max_length=20, choices=item_choices)
    color = models.CharField(max_length=20)
    missing_choices = [(0, "No"), (1, "Yes"), (2, "Found"), (3, "Returned")]
    missing = models.SmallIntegerField(choices=missing_choices, default=0)

    def calculate_price(self):
        price = 0
        if self.item == "sweater":
            price = 20
        elif self.item == "blanket":
            price = 50
        else:
            price = 10
        return price
