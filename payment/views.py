# payment_app/views.py
from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from tenant_app.views.utils import TenantRequiredMixin
from .utils import init_gateway
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib import messages
import datetime

# def item_list(request):
#     items = Item.objects.all()
#     context = {"items": items}
#     return render(request, "item_list.html", context)


# def calculate_total(request):
#     selected_item_ids = request.POST.getlist("selected_items")
#     selected_items = Item.objects.filter(pk__in=selected_item_ids)
#     total_price = sum(item.price for item in selected_items)
#     return render(request, "total_price.html", {"total_price": total_price})


def payment_failed(request):
    # Handle payment failure
    return HttpResponse("Payment Failed")


def payment_cancel(request):
    # Handle payment cancellation
    return HttpResponse("Payment Cancelled")


@csrf_exempt
def payment_notification(request):
    pass


class BookingFeeView(LoginRequiredMixin, DetailView):
    model = models.BookingFee
    template_name = "payment/booking_fee_detail.html"
    context_object_name = "booking_fee"
    

class BookingFeePaymentView(LoginRequiredMixin, View):
    def get(self, request, pk):
        booking_fee = models.BookingFee.objects.get(pk=pk)
        if booking_fee.paid:
            return redirect("tenant:profile")
        
        if booking_fee.room_request.expired():
            messages.error(request, "Your booking request has been expired. Please request again.")
            return redirect("tenant:profile")

        response = init_gateway(request, booking_fee.amount, "Booking Fee", reverse("payment:booking_fee_payment_success", kwargs={"pk": pk}))
        if response["status"] == "SUCCESS":
            return redirect(response["GatewayPageURL"])
        
        return redirect("payment:booking_fee", pk=pk)

@method_decorator(csrf_exempt, name="dispatch")    
class BookingFeePaymentSuccessView(View):
    def post(self, request, pk):
        ipn_data = request.POST
        
        if ipn_data["status"] == "VALID" and ipn_data["tran_id"]:
            transaction_id = ipn_data["tran_id"]


        booking_fee = models.BookingFee.objects.get(pk=pk)
        booking_fee.transaction_id = transaction_id
        booking_fee.paid = True
        booking_fee.date = datetime.datetime.now()
        booking_fee.method = 1
        
        booking_fee.user.is_tenant = True
        booking_fee.user.save()
        tenant = models.Tenant.objects.create(user=booking_fee.user, room=booking_fee.room_request.assigned_room, start_date=booking_fee.room_request.start_date)
        booking_fee.tenant = tenant
        booking_fee.save()

        messages.success(request, "Payment Successful")

        return redirect("tenant:profile")
    

class MonthlyRentListView(TenantRequiredMixin, ListView):
    model = models.Payment
    template_name = "payment/payment_list.html"
    context_object_name = "payments"
    paginate_by = 20
    
    def get_queryset(self):
        return models.Payment.objects.filter(tenant=self.request.user.tenant).order_by("-date")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["booking_fee"] = self.request.user.tenant.booking_fee
        return context


class MonthlyRentView(TenantRequiredMixin, DetailView):
    model = models.Payment
    template_name = "payment/payment_detail.html"
    context_object_name = "payment"


class MonthlyRentPaymentView(TenantRequiredMixin, View):
    def get(self, request, pk):
        payment = models.Payment.objects.get(pk=pk)
        response = init_gateway(request, payment.amount, "Monthly Payment", reverse("payment:monthly_rent_payment_success", kwargs={"pk": pk}))
        if response["status"] == "SUCCESS":
            return redirect(response["GatewayPageURL"])
        
        return redirect("payment:monthly_rent", pk=pk)


@method_decorator(csrf_exempt, name="dispatch")
class MonthlyRentPaymentSuccessView(View):
    def post(self, request, pk):
        ipn_data = request.POST
        
        if ipn_data["status"] == "VALID" and ipn_data["tran_id"]:
            transaction_id = ipn_data["tran_id"]


        payment = models.Payment.objects.get(pk=pk)
        payment.transaction_id = transaction_id
        payment.paid = True
        payment.date = datetime.datetime.now()
        payment.method = 1

        payment.save()

        messages.success(request, "Payment Successful")
        
        return redirect("payment:monthly_rent_list")



# def payment(request):
#     total_price = request.GET.get("total_price")
#     item_names = ", ".join(item.name for item in Item.objects.all())

#     mypayment = SSLCSession(
#         sslc_is_sandbox=True,
#         sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
#         sslc_store_pass=settings.SSLCOMMERZ_STORE_PASSWD,
#     )

#     mypayment.set_urls(
#         success_url=request.build_absolute_uri("/success/"),
#         fail_url=request.build_absolute_uri("/failed/"),
#         cancel_url=request.build_absolute_uri("/cancel/"),
#         ipn_url=request.build_absolute_uri("/payment_notification/"),
#     )

#     mypayment.set_product_integration(
#         total_amount=Decimal(total_price),
#         currency="BDT",
#         product_category="Mixed",
#         product_name=item_names,
#         num_of_item=len(item_names),
#         shipping_method="NO",
#         product_profile="None",
#     )

#     mypayment.set_customer_info(
#         name=request.user.first_name + request.user.last_name,
#         email=request.user.email,
#         address1="SoloNest",
#         address2="SoloNest",
#         city="Dhaka",
#         postcode="1209",
#         country="Bangladesh",
#         phone=request.user.profile.phone_no,
#     )

#     mypayment.set_shipping_info(
#         shipping_to=request.user.first_name + request.user.last_name,
#         address="SoloNest",
#         city="Dhaka",
#         postcode="1209",
#         country="Bangladesh",
#     )

#     response = mypayment.init_payment()

#     if response["status"] == "SUCCESS":
#         return redirect(response["GatewayPageURL"])

#     return redirect("item_list")


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        # Get IPN data
        ipn_data = request.POST

        # Verify IPN data and its authenticity
        # Use your SSLCOMMERZ library's method to verify IPN data
        # Ensure to validate transaction status, transaction amount, etc.

        # Process IPN data and update your records accordingly
        if ipn_data["status"] == "VALID" and ipn_data["tran_id"]:
            # Update your records with transaction ID and other details
            transaction_id = ipn_data["tran_id"]

        # TODO: show success message to the user
        # TODO: make payment paid in your database
    return render(request, "success.html", {"transaction_id": transaction_id})
