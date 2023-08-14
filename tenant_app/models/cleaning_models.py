from django.db import models
from .room_request_models import Tenant, Branch
import datetime as dt


class CleaningSlots(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="cleaning_slots", related_query_name="cleaning_slot")
    time = models.TimeField()
    duration = models.DurationField(default=dt.timedelta(hours=3))

    def __str__(self):
        return f"{self.time} - {(dt.datetime.combine(dt.date(1,1,1),self.time) + self.duration).time()}"


class CleaningRequest(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="cleaning_requests",
        related_query_name="cleaning_request",
    )
    date = models.DateField()
    slot = models.ForeignKey(CleaningSlots, on_delete=models.CASCADE)
    status_choices = [
        (0, "Scheduled"),
        (1, "Completed"),
        (2, "Cancelled (Room Locked)"),
    ]
    status = models.SmallIntegerField(choices=status_choices, default=0)
