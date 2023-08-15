from django.urls import path
from . import views

app_name = "manager"

urlpatterns = [
    path("", views.ManagerDashboardView.as_view(), name="manager_dashboard"),
    path("branch/edit/", views.BranchEditFormView.as_view(), name="branch_edit"),
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
    path("meal/lunch/", views.LunchListView.as_view(), name="lunch_list"),
    path("meals/dinner/", views.DinnerListView.as_view(), name="dinner_list"),
    # path("menu-maker/>", views.MenuMaker.as_view(), name="menu_maker"),
    path("cleaning/", views.CleaningListView.as_view(), name="cleaning_list"),
    path("cleaning/search", views.CleaningSearchView.as_view(), name="cleaning_search"),
    path("cleaning/<int:year>/<int:month>/<int:day>/", views.CleaningListSearchView.as_view(), name="cleaning_list_search"),
    path("cleaning/<int:pk>/complete/", views.CleaningComplete.as_view(), name="cleaning_complete"),
    path("cleaning/<int:pk>/incomplete/", views.CleaningIncomplete.as_view(), name="cleaning_incomplete"),
    path("repair/", views.RepairListView.as_view(), name="repair_list"),
    path(
        "repair/<int:pk>/complete/",
        views.RepairComplete.as_view(),
        name="repair_complete",
    ),
    path("laundry/<str:status>/", views.LaundryListView.as_view(), name="laundry_list"),
    path("laundry/items/<int:pk>/", views.LaundryDetailView.as_view(), name="laundry_detail"),
    path("next-step/<str:status>/", views.LaundryNextStepView.as_view(), name="laundry_next_step"),
    path("missing-laundry/<str:missing>", views.MissingLaundryListView.as_view(), name="missing_laundry_list"),
    path("missing-laundry/<int:pk>/update/", views.MissingLaundryUpdateView.as_view(), name="missing_laundry_update"),
    path("feedback/", views.FeedbackListView.as_view(), name="feedback_list"),
]
