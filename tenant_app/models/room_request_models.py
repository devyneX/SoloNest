from django.db import models
from django.db.models import F, Count, Q
from accounts.models import *
from django.utils import timezone
import datetime


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=11)
    meal_price = models.IntegerField(default=60)
    single_room_base_rent = models.IntegerField(default=8000)
    double_room_base_rent = models.IntegerField(default=5000)
    ac_rent_addition = models.IntegerField(default=500)
    balcony_rent_addition = models.IntegerField(default=500)
    attached_bathroom_rent_addition = models.IntegerField(default=1000)
    cleaning_slot_limit = models.IntegerField(default=5)

    def __str__(self):
        return self.name


class Room(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="rooms",
        related_query_name="room",
    )
    room_no = models.CharField(max_length=10)
    room_type_choices = [(1, "Single"), (2, "Double")]
    room_type = models.SmallIntegerField(choices=room_type_choices)
    ac_choices = [(False, "AC"), (True, "Non-AC")]
    ac = models.BooleanField(choices=ac_choices)
    balcony = models.BooleanField()
    attached_bathroom = models.BooleanField()

    def __str__(self):
        return self.room_no

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

    def get_tenants_count(self):
        return self.tenants.count()


class RoomRequest(models.Model):
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="room_requests",
        related_query_name="room_request",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="room_requests",
        related_query_name="room_request",
    )
    date = models.DateField(default=timezone.now)
    
    start_date = models.DateField()
    
    room_type_choices = [(1, "Single"), (2, "Double")]
    room_type = models.SmallIntegerField(choices=room_type_choices)
    ac_choices = [(False, "AC"), (True, "Non-AC")]
    ac = models.BooleanField(choices=ac_choices)
    balcony = models.BooleanField()
    attached_bathroom = models.BooleanField()
    
    # manager
    assigned_room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, related_name="room_requests", related_query_name="room_request")
    expiry_date = models.DateField(null=True)
    status_choices = [(-1, "Pending"), (1, "Approved"), (0, "Rejected")]
    status = models.SmallIntegerField(choices=status_choices, default=-1)
    rejection_reason = models.CharField(max_length=100, null=True)

    def get_available_rooms(self):
        rooms = Room.objects.filter(
            branch=self.branch,
            room_type=self.room_type,
            ac=self.ac,
            balcony=self.balcony,
            attached_bathroom=self.attached_bathroom,
        )

        rooms = rooms.annotate(tenant_count=Count("tenant"), leaving_tenants=Count("tenant", filter=Q(tenant__leave_request__leave_date__lte=self.start_date)), room_reqs=Count("room_request", filter=Q(room_request__status=1, room_request__expiry_date__gte=datetime.date.today()))) 
        
        rooms = rooms.annotate(empty_slots=F("room_type") - F("tenant_count") - F("room_reqs") + F("leaving_tenants")).filter(empty_slots__gt=0)
        
        return rooms
    
    def expired(self):
        return self.expiry_date and self.expiry_date < datetime.date.today()


class Tenant(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="tenants",
        related_query_name="tenant",
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="tenant",
        related_query_name="tenant",
    )
    start_date = models.DateField()
    lunch_default = models.BooleanField(default=True)
    dinner_default = models.BooleanField(default=True)


    def is_active(self):
        return self.start_date <= datetime.date.today()


class LeaveRequest(models.Model):
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name="leave_request",
        related_query_name="leave_request",
    )
    date = models.DateField(default=timezone.now)
    leave_date = models.DateField()


class ArchivedTenant(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="archived_tenants", related_query_name="archived_tenant")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
