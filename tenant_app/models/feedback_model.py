from django.db import models
from .room_request_models import Tenant
from django.utils import timezone


class Feedback(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    about_choices = [(0, "Meal"), (1, "Cleaning"), (2, "Repair"), (3, "Laundry")]
    about = models.SmallIntegerField(choices=about_choices)
    feedback = models.CharField(max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)
