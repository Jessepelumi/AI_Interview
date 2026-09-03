from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from audit.models import AuditEvent
from .models import Dispute

TRANSITIONS = {
    Dispute.State.DRAFT: {Dispute.State.SUBMITTED},
    Dispute.State.SUBMITTED: {Dispute.State.EVIDENCE_REQUIRED, Dispute.State.WON, Dispute.State.LOST},
    Dispute.State.EVIDENCE_REQUIRED: {Dispute.State.SUBMITTED, Dispute.State.WON, Dispute.State.LOST},
    Dispute.State.WON: {Dispute.State.CLOSED},
    Dispute.State.LOST: {Dispute.State.CLOSED},
}

def validate_amount(payment, amount):
    if float(amount) <= 0 or float(amount) > float(payment.amount):
        raise ValueError("Dispute amount is outside the captured amount")

@transaction.atomic
def transition(dispute, target_state, actor=None, metadata=None):
    if target_state not in TRANSITIONS.get(dispute.state, set()) and target_state != Dispute.State.CLOSED:
        raise ValueError(f"Cannot move {dispute.state} to {target_state}")
    dispute.state = target_state
    dispute.save(update_fields=["state", "updated_at"])
    AuditEvent.objects.create(dispute_id=dispute.id, action=f"state:{target_state}", actor=actor, metadata=metadata or {})
    return dispute

def deadline_has_passed(dispute):
    if not dispute.response_due_at:
        return False
    return dispute.response_due_at.date() < timezone.localdate()
