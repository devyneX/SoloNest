from django.contrib import admin
from .models import *


# Register your models here.
# class TenantAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "phone_no",
#         "blood_group",
#         "emergency_contact",
#         "meal_default",
#     )


# class ApprovalAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "phone_no",
#         "blood_group",
#         "emergency_contact",
#         "meal_default",
#         "room",
#     )
#     list_filter = ("room__number",)

#     def get_queryset(self, request):
#         tenants = super().get_queryset(request)
#         return tenants.filter(room__number__isnull=True)


# class RoomAdmin(admin.ModelAdmin):
#     list_display = (
#         "number",
#         "single",
#         "ac",
#         "balcony",
#         "attached_bathroom",
#         "rent",
#     )
#     list_filter = (
#         "single",
#         "ac",
#         "balcony",
#         "attached_bathroom",
#     )


# admin.site.register(Tenant, TenantAdmin)
# admin.site.register(Room, RoomAdmin)
