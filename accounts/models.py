from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# class Room(models.Model):
#     number = models.IntegerField()
#     single = models.BooleanField()
#     ac = models.BooleanField()
#     balcony = models.BooleanField()
#     attached_bathroom = models.BooleanField()
#     rent = models.IntegerField(default=None, null=True)

#     def __str__(self):
#         return f"Room-{self.number}, Rent-{self.rent}"

#     def save(self, *args, **kwargs):
#         self.rent = 5000 if self.single else 8000
#         if self.ac:
#             self.rent += 1000
#         if self.balcony:
#             self.rent += 500
#         if self.attached_bathroom:
#             self.rent += 1000
#         return super().save(*args, **kwargs)


class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    phone_no = models.CharField(max_length=11)
    blood_group = models.CharField(max_length=3)
    emergency_contact = models.CharField(max_length=11)
    meal_default = models.BooleanField(default=True)


class RoomRequest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    single = models.BooleanField()
    ac = models.BooleanField()
    balcony = models.BooleanField()
    attached_bathroom = models.BooleanField()
    approved = models.BooleanField(default=False)
    # assigned_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    sign_up_link = models.CharField(max_length=100, null=True)
