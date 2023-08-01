from django.shortcuts import render
from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from manager_app import models


class UserListView(ManagerRequiredMixin, ListView):
    model = models.User
    template_name = "manager_app/manager_user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return models.User.objects.filter(is_manager=False, is_superuser=False)


class UserDetailView(ManagerRequiredMixin, DetailView):
    model = models.User
    template_name = "manager_app/manager_user_detail.html"
    context_object_name = "user"


# NOTE: Not used
class UserUpdateView(ManagerRequiredMixin, UpdateView):
    model = models.User
    template_name = "manager_app/manager_user_update.html"
    context_object_name = "user"


# NOTE: Not used
class UserDeleteView(ManagerRequiredMixin, DeleteView):
    model = models.User
    template_name = "manager_app/manager_user_delete.html"
    context_object_name = "user"
