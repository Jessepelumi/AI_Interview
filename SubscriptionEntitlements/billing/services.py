from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from .models import BillingEvent, Payment, Subscription


@transaction.atomic
def apply_invoice_paid(provider, payload):
    event, created = BillingEvent.objects.get_or_create(
        external_event_id=payload["id"],
        defaults={"provider": provider, "event_type": payload["type"]},
    )
    if not created:
        return event, False

    subscription = Subscription.objects.get(
        external_reference=payload["data"]["subscription_id"]
    )
    Payment.objects.create(
        event=event,
        subscription=subscription,
        amount=Decimal(payload["data"]["amount_minor"]),
        currency=payload["data"]["currency"],
    )
    subscription.status = Subscription.Status.ACTIVE
    subscription.save(update_fields=["status"])
    event.processed_at = timezone.now()
    event.save(update_fields=["processed_at"])
    return event, True
