from django.views.generic import TemplateView
from .utils import ManagerRequiredMixin
from .user_views import *
from .tenant_views import *
from .room_views import *
from .room_request_views import *
from .meal_views import *
from .cleaning_views import *
from .repair_views import *
from .laundry_views import *


class ManagerDashboardView(ManagerRequiredMixin, TemplateView):
    template_name = "manager_app/manager_dashboard.html"
