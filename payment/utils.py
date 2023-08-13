from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.conf import settings
from django.urls import reverse


def init_gateway(request, price, item_name, success_url):
    mypayment = SSLCSession(
        sslc_is_sandbox=True,
        sslc_store_id=settings.SSLCOMMERZ_STORE_ID,
        sslc_store_pass=settings.SSLCOMMERZ_STORE_PASSWD,
    )

    mypayment.set_urls(
        success_url=request.build_absolute_uri(success_url),
        fail_url=request.build_absolute_uri(reverse("payment:payment_failed")),
        cancel_url=request.build_absolute_uri(reverse("payment:payment_cancel")),
        ipn_url=request.build_absolute_uri(reverse("payment:payment_notification")),
    )

    mypayment.set_product_integration(
        total_amount=Decimal(price),
        currency="BDT",
        product_category="Mixed",
        product_name=item_name,
        num_of_item=1,
        shipping_method="NO",
        product_profile="None",
    )

    mypayment.set_customer_info(
        name=request.user.first_name + request.user.last_name,
        email=request.user.email,
        address1="SoloNest",
        address2="SoloNest",
        city="Dhaka",
        postcode="1209",
        country="Bangladesh",
        phone=request.user.profile.phone_no,
    )

    mypayment.set_shipping_info(
        shipping_to=request.user.first_name + request.user.last_name,
        address="SoloNest",
        city="Dhaka",
        postcode="1209",
        country="Bangladesh",
    )

    response = mypayment.init_payment()

    return response