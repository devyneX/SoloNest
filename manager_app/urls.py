from django.urls import path
from . import views

app_name = "manager"

urlpatterns = [
    path("", views.ManagerDashboardView.as_view(), name="manager_dashboard"),
    path("brach/edit/", views.BranchEditFormView.as_view(), name="branch_edit"),
    path(
        "cleaning_slot/edit/",
        views.CleaningSlotEditFormView.as_view(),
        name="cleaning_slot_edit",
    ),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path(
        "users/<int:pk>/update/",
        views.UserUpdateView.as_view(),
        name="user_update",
    ),
    path(
        "users/<int:pk>/delete/",
        views.UserDeleteView.as_view(),
        name="user_delete",
    ),
    path("tenants/", views.TenantListView.as_view(), name="tenant_list"),
    path(
        "tenants/<int:pk>/",
        views.TenantDetailView.as_view(),
        name="tenant_detail",
    ),
    path(
        "tenants/<int:pk>/update/",
        views.TenantUpdateView.as_view(),
        name="tenant_update",
    ),
    path(
        "tenants/<int:pk>/delete/",
        views.TenantDeleteView.as_view(),
        name="tenant_delete",
    ),
    path("rooms/", views.RoomListView.as_view(), name="room_list"),
    path("rooms/<int:pk>/", views.RoomDetailView.as_view(), name="room_detail"),
    path(
        "rooms/<int:pk>/update/",
        views.RoomUpdateView.as_view(),
        name="room_update",
    ),
    path(
        "rooms/<int:pk>/delete/",
        views.RoomDeleteView.as_view(),
        name="room_delete",
    ),
    path(
        "room-requests/",
        views.RoomRequestListView.as_view(),
        name="room_request_list",
    ),
    path(
        "room-requests/<int:pk>/",
        views.RoomRequestDetailView.as_view(),
        name="room_request_detail",
    ),
    path(
        "room-requests/<int:pk>/approve/",
        views.RoomRequestApprovalView.as_view(),
        name="room_request_approve",
    ),
    path(
        "room-requests/<int:pk>/reject/",
        views.RoomRequestRejectionView.as_view(),
        name="room_request_reject",
    ),
    path("lunch-list/", views.LunchListView.as_view(), name="lunch_list"),
    path("dinner-list/", views.DinnerListView.as_view(), name="dinner_list"),
    # path("menu-maker/>", views.MenuMaker.as_view(), name="menu_maker"),
    path("cleaning-list/", views.CleaningListView.as_view(), name="cleaning_list"),
    path("repair-list/", views.RepairListView.as_view(), name="repair_list"),
    path(
        "repair-complete/<int:pk>/",
        views.RepairComplete.as_view(),
        name="repair_complete",
    ),
    path("laundry-list/", views.LaundryListView.as_view(), name="laundry_list"),
    path("feedback-list/", views.FeedbackListView.as_view(), name="feedback_list"),
]
