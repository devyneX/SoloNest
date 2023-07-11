from django.db import models
from accounts.models import User, Profile


# Create your models here.
class Branch(models.Model):
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11)


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
        rent = 5000 if self.room_type == "single" else 8000
        rent += 500 if self.ac else 0
        rent += 500 if self.balcony else 0
        rent += 1000 if self.attached_bathroom else 0
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


class Tenant(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def calculate_payment(self):
        payment = self.room.calculate_rent()
        return payment
