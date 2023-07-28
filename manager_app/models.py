from django.db import models
from accounts.models import *
from tenant_app.models import *


# Create your models here.
class Manager(models.Model):
    branch = models.OneToOneField(Branch, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
