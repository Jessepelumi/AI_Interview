from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Membership, Organisation
from payments.models import Payment
from disputes.models import Dispute

@pytest.fixture
def case(db):
    user = get_user_model().objects.create_user("agent", password="password")
    org = Organisation.objects.create(name="North Shop", processor_account_id="acct_north")
    Membership.objects.create(user=user, organisation=org, role=Membership.Role.AGENT)
    payment = Payment.objects.create(organisation=org, processor_reference="pay_1", amount=Decimal("100.00"),
        currency="GBP", captured_at=timezone.now(), refundable_amount=Decimal("100.00"))
    dispute = Dispute.objects.create(organisation=org, payment=payment, reason="not_received",
        amount=Decimal("40.00"), created_by=user)
    return user, org, payment, dispute
