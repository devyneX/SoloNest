from django.urls import path
from . import views

urlpatterns = [
    path("test", views.test, name="test"),
    # path("tenant_login", views.TenantLoginView.as_view(), name="tenant_login"),
    # path("room_request", views.RoomRequestView.as_view(), name="room_request"),
]
