from . import views
from django.urls import path


app_name = "tenant"


urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("request-room/", views.RoomRequestView.as_view(), name="room_request"),
    path(
        "room-requests/", views.RoomRequestListView.as_view(), name="room_request_list"
    ),
    path(
        "room-requests/<int:pk>/",
        views.RoomRequestDetailView.as_view(),
        name="room_request_detail",
    ),
    path(
        "room-requests/<int:pk>/update/",
        views.RoomRequestUpdateView.as_view(),
        name="room_request_update",
    ),
    path("request-meal/", views.MealRequestView.as_view(), name="meal_request"),
    path(
        "monthly-meals/", views.MonthlyMealListView.as_view(), name="monthly_meal_list"
    ),
    path(
        "meal-request/<int:pk>/",
        views.MealRequestDetailView.as_view(),
        name="meal_request_detail",
    ),
    path(
        "meal-request/<int:pk>/update/",
        views.MealRequestUpdateView.as_view(),
        name="meal_request_update",
    ),
    path(
        "meal-request/<int:pk>/delete/",
        views.MealRequestDeleteView.as_view(),
        name="meal_delete",
    ),
    path(
        "request-cleaning/",
        views.CleaningRequestView.as_view(),
        name="cleaning_request",
    ),
    path(
        "cleaning-requests/",
        views.CleaningRequestListView.as_view(),
        name="cleaning_request_list",
    ),
    path(
        "cleaning-requests/<int:pk>/",
        views.CleaningRequestDetailView.as_view(),
        name="cleaning_request_detail",
    ),
    path(
        "cleaning-requests/<int:pk>/update/",
        views.CleaningRequestUpdateView.as_view(),
        name="cleaning_request_update",
    ),
    path(
        "cleaning-requests/<int:pk>/delete/",
        views.CleaningRequestDeleteView.as_view(),
        name="cleaning_delete",
    ),
    path(
        "request-laundry/", views.LaundryRequestView.as_view(), name="laundry_request"
    ),
    path(
        "laundry-requests/",
        views.LaundryRequestListView.as_view(),
        name="laundry_request_list",
    ),
    path(
        "laundry-requests/<int:pk>/",
        views.LaundryRequestDetailView.as_view(),
        name="laundry_request_detail",
    ),
    path(
        "laundry-requests/<int:pk>/update/",
        views.LaundryRequestUpdateView.as_view(),
        name="laundry_request_update",
    ),
    path(
        "laundry-requests/<int:pk>/delete/",
        views.LaundryRequestDeleteView.as_view(),
        name="laundry_delete",
    ),
]