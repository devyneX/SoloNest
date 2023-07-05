from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from .models import *


# Register your models here.
@admin.register(RoomRequest)
class RoomRequestAdmin(admin.ModelAdmin):
    # change_list_template = "admin/accounts/room_request_change_list.html"
    list_display = (
        "first_name",
        "last_name",
        "email",
        "single",
        "ac",
        "balcony",
        "attached_bathroom",
        "approved",
        "sign_up_link",
        "room_request_actions",
    )
    readonly_fields = (
        "first_name",
        "last_name",
        "email",
        "single",
        "ac",
        "balcony",
        "attached_bathroom",
        "approved",
        "sign_up_link",
        "room_request_actions",
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "approve/<int:id>",
                self.admin_site.admin_view(self.approve),
                name="approve",
            ),
        ]
        return custom_urls + urls

    def room_request_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Approve</a>&nbsp;',
            reverse("admin:approve", args=[obj.pk]),
        )

    room_request_actions.short_description = "Action"
    room_request_actions.allow_tags = True

    def approve(self, request, id):
        req = RoomRequest.objects.get(id=id)
        req.approved = True
        req.sign_up_link = reverse("tenant_signup", args=[req.id])
        req.save()
        if req:
            send_mail(
                "Room Request Approved",
                f"Your room request has been approved. Please sign up to complete the process at {req.sign_up_link}",
                settings.EMAIL_HOST_USER,
                [req.email],
                fail_silently=False,
            )
            return redirect("admin:accounts_roomrequest_changelist")
        else:
            return redirect("admin:accounts_roomrequest_changelist")


# admin.site.register(Tenant)
# admin.site.register(Room)
