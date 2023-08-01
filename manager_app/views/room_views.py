from django.shortcuts import render
from .utils import ManagerRequiredMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from manager_app import models


# NOTE: might use
class RoomCreateView(ManagerRequiredMixin, CreateView):
    model = models.Room
    template_name = "manager_app/manager_room_create.html"
    context_object_name = "room"


class RoomListView(ManagerRequiredMixin, ListView):
    model = models.Room
    template_name = "manager_app/manager_room_list.html"
    context_object_name = "rooms"


class RoomDetailView(ManagerRequiredMixin, DetailView):
    model = models.Room
    template_name = "manager_app/manager_room_detail.html"
    context_object_name = "room"


class RoomUpdateView(ManagerRequiredMixin, UpdateView):
    model = models.Room
    template_name = "manager_app/manager_room_update.html"
    context_object_name = "room"


class RoomDeleteView(ManagerRequiredMixin, DeleteView):
    model = models.Room
    template_name = "manager_app/manager_room_delete.html"
    context_object_name = "room"
