from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("room-request", views.RoomRequestView.as_view(), name="room_request"),
    path(
        "tenant-signup/<int:pk>", views.TenantSignUpView.as_view(), name="tenant_signup"
    ),
    path("tenant-login", views.TenantLoginView.as_view(), name="tenant_login")
    # path("tenant-update/<pk>", views.TenantUpdateView.as_view(), name="update"),
]
