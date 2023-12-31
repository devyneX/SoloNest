from django.views.generic import TemplateView, UpdateView
from django.views import View
from .utils import ManagerRequiredMixin
from .user_views import *
from .tenant_views import *
from .room_views import *
from .room_request_views import *
from .meal_views import *
from .cleaning_views import *
from .repair_views import *
from .laundry_views import *
from .feedback_views import *
from manager_app import models


class ManagerDashboardView(ManagerRequiredMixin, TemplateView):
    template_name = "manager_app/manager_dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branch"] = self.request.user.manager.branch
        tenant_count = models.Tenant.objects.filter(
            room__branch=self.request.user.manager.branch
        ).count()
        room_count = models.Room.objects.filter(
            branch=self.request.user.manager.branch
        ).count()
        room_request_count = models.RoomRequest.objects.filter(
            branch=self.request.user.manager.branch, status=-1
        ).count()
        repair_count = models.RepairRequest.objects.filter(
            tenant__room__branch=self.request.user.manager.branch, completed=False
        ).count()
        missing_laundry_count = models.LaundryItem.objects.filter(
            laundry_request__tenant__room__branch=self.request.user.manager.branch, missing=1
        ).count()
        context["tenant_count"] = tenant_count
        context["room_count"] = room_count
        context["room_request_count"] = room_request_count
        context["repair_count"] = repair_count
        context["missing_laundry_count"] = missing_laundry_count
        return context


class BranchEditFormView(ManagerRequiredMixin, UpdateView):
    model = models.Branch
    fields = [
        "meal_price",
        "single_room_base_rent",
        "double_room_base_rent",
        "ac_rent_addition",
        "balcony_rent_addition",
        "attached_bathroom_rent_addition",
        "cleaning_slot_limit",
    ]
    template_name = "manager_app/branch_edit.html"
    success_url = reverse_lazy("manager:manager_dashboard")

    def get_object(self, queryset=None):
        return self.request.user.manager.branch


class SendOutBillsView(ManagerRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        branch = self.request.user.manager.branch
        today = datetime.date.today()
        leaving_tenants = models.Tenant.objects.filter(room__branch=branch, leave_request__date__lte=today)
        for tenant in leaving_tenants:
            archived = models.ArchivedTenant.objects.create(user=tenant.user, room=tenant.room, start_date=tenant.start_date, end_date=tenant.leave_request.date)
            models.Payment.objects.filter(tenant=tenant).update(archived=archived)
            tenant.booking_fee.archived = archived
            tenant.booking_fee.save()

            tenant.user.is_tenant = False

            tenant.user.save()

            tenant.delete()

        tenants = models.Tenant.objects.filter(room__branch=branch, start_date__lte=today)
        for tenant in tenants:
            if models.Payment.objects.filter(tenant=tenant, month=today.month, year=today.year).exists():
                continue
            bill = models.Payment.objects.create(tenant=tenant, month=today.month, year=today.year)
            bill.get_amount()
            bill.save()
        return redirect("manager:manager_dashboard")