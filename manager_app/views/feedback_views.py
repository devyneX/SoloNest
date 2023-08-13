from django.views.generic import ListView
from manager_app import models
from .utils import ManagerRequiredMixin


class FeedbackListView(ManagerRequiredMixin, ListView):
    model = models.Feedback
    template_name = "manager_app/manager_feedback_list.html"
    context_object_name = "feedbacks"
    paginate_by = 10
