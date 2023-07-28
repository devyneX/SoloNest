from django.db import models
from .room_request_models import Tenant


class CleaningSlots(models.Model):
    time = models.TimeField()
    duration = models.DurationField()


class CleaningRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.ForeignKey(CleaningSlots, on_delete=models.CASCADE)
    status_choices = [(0, "Scheduled"), (1, "Completed")]
    status = models.SmallIntegerField(choices=status_choices, default=0)
