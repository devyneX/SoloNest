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
        print(self.request.user.manager.branch)
        context["branch"] = self.request.user.manager.branch
        context["tenant_count"] = models.Tenant.objects.filter(
            room__branch=self.request.user.manager.branch
        ).count()
        context["room_count"] = models.Room.objects.filter(
            branch=self.request.user.manager.branch
        ).count()
        context["room_request_count"] = models.RoomRequest.objects.filter(
            branch=self.request.user.manager.branch
        ).count()
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
    success_url = "/manager/dashboard/"

    def get_object(self, queryset=None):
        return self.request.user.manager.branch

