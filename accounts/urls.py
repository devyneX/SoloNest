from django.urls import path
from . import views

urlpatterns = [
    # path("test", views.test, name="test"),
    path("room-request", views.RoomRequestView.as_view(), name="room_request"),
    path("tenant-signup/<int:id>", views.TenantSignUp.as_view(), name="tenant_signup"),
]
