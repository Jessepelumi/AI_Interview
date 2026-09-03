from dataclasses import dataclass
from decimal import Decimal

from django.utils import timezone
from django.db import transaction

from .models import Account, WebhookEvent


@dataclass(frozen=True)
class ProcessingResult:
    applied: bool
    reason: str


def apply_provider_event(payload):
    """Apply a trusted, schema-validated provider webhook."""
    with transaction.atomic():
        event, created = WebhookEvent.objects.get_or_create(
            provider_event_id=payload["id"],
            defaults={"event_type": payload["type"]},
        )
        if not created:
            return ProcessingResult(applied=False, reason="duplicate")

        if payload["type"] != "credit.applied":
            return ProcessingResult(applied=False, reason="ignored")

        account = Account.objects.get(external_id=payload["data"]["account_id"])
        amount = (Decimal(payload["data"]["amount_minor"]) / Decimal("100")).quantize(Decimal("0.01"))
        account.balance += amount
        account.save(update_fields=["balance"])

        event.processed_at = timezone.now()
        event.save(update_fields=["processed_at"])
        return ProcessingResult(applied=True, reason="applied")

