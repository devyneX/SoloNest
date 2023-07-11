from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Branch)
admin.site.register(models.Room)
admin.site.register(models.RoomRequest)
admin.site.register(models.Tenant)
