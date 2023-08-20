from django.db import models
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .utils import TenantRequiredMixin
from tenant_app import models, forms 


class LeaveRequestView(TenantRequiredMixin, CreateView):
    model = models.LeaveRequest
    form_class = forms.LeaveRequestForm
    template_name = 'tenant_app/leave_request.html'
    success_url = reverse_lazy('tenant:profile')

    def get(self, request, *args, **kwargs):
        if models.LeaveRequest.objects.filter(tenant=self.request.user.tenant).exists():
            return redirect(reverse('tenant:profile'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)
