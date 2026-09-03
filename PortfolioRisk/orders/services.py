from django.db import transaction

from risk.services import evaluate_order

from .models import Order


@transaction.atomic
def submit_order(portfolio, instrument, side, quantity, client_order_id, as_of):
    order, created = Order.objects.get_or_create(
        portfolio=portfolio,
        client_order_id=client_order_id,
        defaults={
            "instrument": instrument,
            "side": side,
            "quantity": quantity,
        },
    )
    if created:
        evaluate_order(order, as_of)
        order.status = Order.Status.ACCEPTED
        order.save(update_fields=["status"])
    return order, created
