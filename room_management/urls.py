from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("update-profile/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("request-room/", views.RoomRequestView.as_view(), name="room_request"),
    path(
        "room-requests/",
        views.RoomRequestListView.as_view(),
        name="room_request_list",
    ),
    path(
        "room-requests/<int:pk>/details",
        views.RoomRequestDetailView.as_view(),
        name="room_request_detail",
    ),
    path(
        "room-requests/<int:pk>/update/",
        views.RoomRequestUpdateView.as_view(),
        name="room_request_update",
    ),
    path(
        "room-request/<int:pk>/delete/",
        views.RoomRequestDeleteView.as_view(),
        name="room_request_delete",
    ),
]
