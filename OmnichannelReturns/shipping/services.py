from decimal import Decimal

from django.conf import settings


def select_carrier(return_request):
    country = return_request.receiving_location.country_code.lower()
    return settings.RETURN_CARRIER_BY_COUNTRY.get(
        country, settings.RETURN_CARRIER_BY_COUNTRY["DEFAULT"]
    )


def build_label_payload(return_request):
    weight_grams = sum(
        line.order_line.product.weight_grams * line.units
        for line in return_request.lines.select_related("order_line__product")
    )
    return {
        "carrier": select_carrier(return_request),
        "weight_kg": f"{Decimal(weight_grams):.3f}",
        "reference": f"return-{return_request.id}",
    }
