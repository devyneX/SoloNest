from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from tenant_app.models import *

# from django.views.generic.edit import FormView
from .utils import TenantRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy


class FeedbackView(TenantRequiredMixin, CreateView):
    model = Feedback
    fields = ["about", "feedback"]
    template_name = "tenant_app/feedback.html"
    success_url = reverse_lazy("tenant:profile")
    
    def form_valid(self, form):
        # TODO: show message
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)
    