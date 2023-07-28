from django.db import models
from .room_request_models import Tenant


class RepairRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
