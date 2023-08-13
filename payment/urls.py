# payment_app/urls.py
from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    # path("", views.item_list, name="item_list"),
    # path("calculate_total/", views.calculate_total, name="calculate_total"),
    # path("payment/", views.payment, name="payment"),
    path("success/", views.payment_success, name="payment_success"),
    path("failed/", views.payment_failed, name="payment_failed"),
    path("cancel/", views.payment_cancel, name="payment_cancel"),
    path(
        "payment_notification/", views.payment_notification, name="payment_notification"
    ),
    path("booking_fee/<int:pk>/", views.BookingFeeView.as_view(), name="booking_fee"),
    path("booking_fee/<int:pk>/payment/", views.BookingFeePaymentView.as_view(), name="booking_fee_payment"),
    path("booking_fee/<int:pk>/success/", views.BookingFeePaymentSuccessView.as_view(), name="booking_fee_payment_success"),
    path("monthly_rent/<int:pk>/", views.MonthlyRentView.as_view(), name="monthly_rent"),
    path("monthly_rent/<int:pk>/payment/", views.MonthlyRentPaymentView.as_view(), name="monthly_rent_payment"),
    path("monthly_rent/<int:pk>/success/", views.MonthlyRentPaymentSuccessView.as_view(), name="monthly_rent_payment_success"),
]
