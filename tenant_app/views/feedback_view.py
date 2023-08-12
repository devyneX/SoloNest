from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from tenant_app.models import *

# from django.views.generic.edit import FormView
from .utils import TenantRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy

# def feedback_view(request):
#     if request.method == 'POST':
#         form = FeedbackForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect or show a success message
#             return redirect('success_page_or_some_url')
#     else:
#         form = FeedbackForm()
#     return render(request, 'feedback.html', {'form': form})

class FeedbackView(TenantRequiredMixin, CreateView):
    model = Feedback
    fields = ["about", "feedback"]
    template_name = "tenant_app/feedback.html"
    success_url = reverse_lazy("tenant:profile")
    
    def form_valid(self, form):
        # TODO: show message
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)
    