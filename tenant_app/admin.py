from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Branch)
admin.site.register(models.Room)
admin.site.register(models.RoomRequest)
admin.site.register(models.Tenant)
admin.site.register(models.Meal)
admin.site.register(models.MealMonthlyMenu)
admin.site.register(models.CleaningRequest)
admin.site.register(models.CleaningSlots)
admin.site.register(models.RepairRequest)
admin.site.register(models.LaundryRequest)
admin.site.register(models.LaundryItem)

