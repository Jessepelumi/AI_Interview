import pytest
from rest_framework.test import APIClient
from accounts.models import Organisation
from disputes.models import Dispute

pytestmark = pytest.mark.django_db

def test_list_is_scoped_to_memberships(case):
    user, _, payment, _ = case
    other = Organisation.objects.create(name="South Shop", processor_account_id="acct_south")
    Dispute.objects.create(organisation=other, payment=payment, reason="fraud", amount="1.00", created_by=user)
    client = APIClient(); client.force_authenticate(user)
    response = client.get("/api/disputes/")
    assert response.status_code == 200
    assert response.data["count"] == 1

def test_detail_is_scoped_to_memberships(case):
    user, _, payment, _ = case
    other = Organisation.objects.create(name="South Shop", processor_account_id="acct_south")
    foreign = Dispute.objects.create(organisation=other, payment=payment, reason="fraud", amount="1.00", created_by=user)
    client = APIClient(); client.force_authenticate(user)
    assert client.get(f"/api/disputes/{foreign.id}/").status_code == 404
