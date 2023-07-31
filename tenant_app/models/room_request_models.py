from django.db import models
from accounts.models import *


class Branch(models.Model):
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11)
    meal_price = models.IntegerField(default=60)
    single_room_base_rent = models.IntegerField(default=8000)
    double_room_base_rent = models.IntegerField(default=5000)
    ac_rent_addition = models.IntegerField(default=500)
    balcony_rent_addition = models.IntegerField(default=500)
    attached_bathroom_rent_addition = models.IntegerField(default=1000)
    cleaning_slot_limit = models.IntegerField(default=5)


class Room(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=10)
    room_type_choices = [("single", "Single"), ("double", "Double")]
    room_type = models.CharField(max_length=10, choices=room_type_choices)
    ac_choices = [(False, "AC"), (True, "Non-AC")]
    ac = models.BooleanField(choices=ac_choices)
    balcony = models.BooleanField()
    attached_bathroom = models.BooleanField()

    def calculate_rent(self):
        if self.room_type == "single":
            rent = self.branch.single_room_base_rent
        else:
            rent = self.branch.double_room_base_rent

        rent += self.branch.ac_rent_addition if self.ac else 0
        rent += self.branch.balcony_rent_addition if self.balcony else 0
        rent += (
            self.branch.attached_bathroom_rent_addition if self.attached_bathroom else 0
        )

        return rent


class RoomRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_type_choices = [("single", "Single"), ("double", "Double")]
    room_type = models.CharField(max_length=10, choices=room_type_choices)
    ac_choices = [(False, "AC"), (True, "Non-AC")]
    ac = models.BooleanField(choices=ac_choices)
    balcony = models.BooleanField()
    attached_bathroom = models.BooleanField()
    # manager
    assigned_room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    status_choices = [(-1, "Pending"), (1, "Approved"), (0, "Rejected")]
    status = models.SmallIntegerField(choices=status_choices, default=-1)
    rejection_reason = models.CharField(max_length=100, null=True)


class Tenant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lunch_default = models.BooleanField(default=True)
    dinner_default = models.BooleanField(default=True)

    def calculate_payment(self):
        payment = self.room.calculate_rent()
        return payment
