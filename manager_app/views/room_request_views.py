from .utils import ManagerRequiredMixin
from django.views.generic import ListView, DetailView, FormView
from manager_app import models, forms


class RoomRequestListView(ManagerRequiredMixin, ListView):
    model = models.RoomRequest
    template_name = "manager_app/manager_room_request_list.html"
    context_object_name = "room_requests"

    def get_queryset(self):
        return self.model.objects.filter(status=-1)

    def get_context_data(self, **kwargs):
        room_requests = super().get_context_data(**kwargs)["room_requests"]
        context = {"room_requests": []}
        for room_request in room_requests:
            no_of_available_rooms = models.Room.objects.filter(
                room_type=room_request.room_type,
                ac=room_request.ac,
                balcony=room_request.balcony,
                attached_bathroom=room_request.attached_bathroom,
            ).count()
            context["room_requests"].append((room_request, no_of_available_rooms))

        print(context)
        return context


class RoomRequestDetailView(ManagerRequiredMixin, DetailView):
    model = models.RoomRequest
    template_name = "manager_app/manager_room_request_detail.html"
    context_object_name = "room_request"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_request = context["room_request"]
        no_of_available_rooms = models.Room.objects.filter(
            room_type=room_request.room_type,
            ac=room_request.ac,
            balcony=room_request.balcony,
            attached_bathroom=room_request.attached_bathroom,
        ).count()
        context["no_of_available_rooms"] = no_of_available_rooms
        return context


class RoomRequestApprovalView(ManagerRequiredMixin, FormView):
    form = forms.RoomRequestApprovalForm
    template_name = "manager_app/manager_room_request_approval.html"

    def form_valid(self, form):
        room_request = models.RoomRequest.objects.get(pk=self.kwargs["pk"])
        room_request.status = 1
        room_request.room = form.cleaned_data["room"]
        room_request.save()
        return super().form_valid(form)


class RoomRequestRejectionView(ManagerRequiredMixin, FormView):
    form = forms.RoomRequestRejectionForm
    template_name = "manager_app/manager_room_request_rejection.html"

    def form_valid(self, form):
        room_request = models.RoomRequest.objects.get(pk=self.kwargs["pk"])
        room_request.status = 0
        room_request.rejection_reason = form.cleaned_data["rejection_reason"]
        room_request.save()
        return super().form_valid(form)
