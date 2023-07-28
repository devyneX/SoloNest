from django.db import models
from .room_request_models import Tenant


class LaundryRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)


class LaundryItem(models.Model):
    laundry_request = models.ForeignKey(LaundryRequest, on_delete=models.CASCADE)
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
    missing = models.BooleanField(default=False)
    missing_date = models.DateField(null=True, blank=True)

    # manager
    found = models.BooleanField(default=False)
    found_date = models.DateField(null=True, blank=True)

    def calculate_price(self):
        price = 0
        if self.item == "sweater":
            price = 20
        elif self.item == "blanket":
            price = 50
        else:
            price = 10
        return price