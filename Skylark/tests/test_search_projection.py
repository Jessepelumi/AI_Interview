import pytest
from django.urls import reverse
from search_index.services import apply_index_event, build_index_event
from sharing.models import Grant
from sharing.services import revoke_grant
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db

def test_authorized_document_appears_in_search(api_client, scenario):
    s = scenario
    Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    apply_index_event(build_index_event(s["document"]).as_payload())
    authenticate(api_client, s["reader"])
    response = api_client.get(reverse("search"), {"q": "Aurora"})
    assert [item["id"] for item in response.data["results"]] == [str(s["document"].id)]

def test_older_index_event_cannot_restore_revoked_visibility(api_client, scenario):
    s = scenario
    grant = Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    old_event = build_index_event(s["document"]).as_payload()
    revoke_grant(grant)
    s["document"].refresh_from_db()
    apply_index_event(build_index_event(s["document"]).as_payload())
    apply_index_event(old_event)  # delayed delivery after the newer ACL event
    authenticate(api_client, s["reader"])
    response = api_client.get(reverse("search"), {"q": "Aurora"})
    assert response.data["results"] == []

def test_current_revocation_event_removes_search_result(api_client, scenario):
    s = scenario
    grant = Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    apply_index_event(build_index_event(s["document"]).as_payload())
    revoke_grant(grant)
    s["document"].refresh_from_db()
    apply_index_event(build_index_event(s["document"]).as_payload())
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("search"), {"q": "Aurora"}).data["results"] == []
