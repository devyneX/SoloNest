# payment_app/views.py
from django.shortcuts import render
from .models import Item
from django.shortcuts import redirect
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def item_list(request):
    items = Item.objects.all()
    context = {"items": items}
    return render(request, "item_list.html", context)


def calculate_total(request):
    selected_item_ids = request.POST.getlist("selected_items")
    selected_items = Item.objects.filter(pk__in=selected_item_ids)
    total_price = sum(item.price for item in selected_items)
    return render(request, "total_price.html", {"total_price": total_price})


def payment_failed(request):
    # Handle payment failure
    return HttpResponse("Payment Failed")


def payment_cancel(request):
    # Handle payment cancellation
    return HttpResponse("Payment Cancelled")


@csrf_exempt
def payment_notification(request):
    pass


def payment(request):
    total_price = request.GET.get("total_price")
    item_names = ", ".join(item.name for item in Item.objects.all())

    mypayment = SSLCSession(
        sslc_is_sandbox=True,
        sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
        sslc_store_pass=settings.SSLCOMMERZ_STORE_PASSWD,
    )

    mypayment.set_urls(
        success_url=request.build_absolute_uri("/success/"),
        fail_url=request.build_absolute_uri("/failed/"),
        cancel_url=request.build_absolute_uri("/cancel/"),
        ipn_url=request.build_absolute_uri("/payment_notification/"),
    )

    mypayment.set_product_integration(
        total_amount=Decimal(total_price),
        currency="BDT",
        product_category="clothing",
        product_name=item_names,
        num_of_item=len(item_names),
        shipping_method="YES",
        product_profile="None",
    )

    mypayment.set_customer_info(
        name="John Doe",
        email="johndoe@email.com",
        address1="demo address",
        address2="demo address 2",
        city="Dhaka",
        postcode="1207",
        country="Bangladesh",
        phone="01711111111",
    )

    mypayment.set_shipping_info(
        shipping_to="demo customer",
        address="demo address",
        city="Dhaka",
        postcode="1209",
        country="Bangladesh",
    )

    response = mypayment.init_payment()

    if response["status"] == "SUCCESS":
        return redirect(response["GatewayPageURL"])

    return redirect("item_list")


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
    return render(request, "success.html", {"transaction_id": transaction_id})
