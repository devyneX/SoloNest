from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .utils import TenantRequiredMixin
from tenant_app import models, forms 


class LeaveRequestView(TenantRequiredMixin, CreateView):
    model = models.LeaveRequest
    fields = ["leave_date"]
    template_name = 'leave_request.html'
    success_url = reverse_lazy('tenant_app:')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leave_request'] = models.LeaveRequest.objects.filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)