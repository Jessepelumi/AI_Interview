import pytest
from audit.models import AuditEvent
from disputes.models import Dispute
from disputes.services import transition, validate_amount

pytestmark = pytest.mark.django_db

def test_submit_writes_audit_event(case):
    user, _, _, dispute = case
    transition(dispute, Dispute.State.SUBMITTED, user)
    assert dispute.state == Dispute.State.SUBMITTED
    assert AuditEvent.objects.filter(dispute_id=dispute.id, action="state:submitted").exists()

def test_amount_must_be_positive(case):
    _, _, payment, _ = case
    with pytest.raises(ValueError):
        validate_amount(payment, 0)

def test_draft_cannot_be_closed(case):
    _, _, _, dispute = case
    with pytest.raises(ValueError):
        transition(dispute, Dispute.State.CLOSED)
