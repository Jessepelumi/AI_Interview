from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from django.db.models import Sum

from inventory.models import StockLevel

from .models import ReturnLine, ReturnRequest

PENNY = Decimal("0.01")


def calculate_refund(order_line, units):
    return (order_line.unit_price * units).quantize(PENNY, rounding=ROUND_HALF_UP)


def validate_return_quantity(order_line, units):
    already_returned = (
        ReturnLine.objects.filter(order_line=order_line).aggregate(total=Sum("units"))["total"]
        or 0
    )
    if already_returned + units > order_line.quantity:
        raise ValueError("return quantity exceeds purchased quantity")


@transaction.atomic
def process_return(return_request):
    if return_request.status == ReturnRequest.Status.COMPLETED:
        return return_request
    for line in return_request.lines.select_related(
        "order_line__product", "order_line__fulfilment_location"
    ):
        stock, _ = StockLevel.objects.get_or_create(
            location=line.order_line.fulfilment_location,
            product=line.order_line.product,
            defaults={"on_hand": 0},
        )
        stock.on_hand += line.units
        stock.save(update_fields=["on_hand"])
    return_request.status = ReturnRequest.Status.COMPLETED
    return_request.save(update_fields=["status"])
    return return_request
