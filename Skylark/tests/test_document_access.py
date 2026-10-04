import pytest
from django.urls import reverse
from sharing.models import Grant
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db

def test_direct_grant_allows_document_read(api_client, scenario):
    s = scenario
    Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    authenticate(api_client, s["reader"])
    response = api_client.get(reverse("document-detail", args=[s["document"].id]))
    assert response.status_code == 200
    assert response.data["title"] == "Project Aurora"

def test_unshared_document_is_hidden(api_client, scenario):
    s = scenario
    authenticate(api_client, s["outsider"])
    response = api_client.get(reverse("document-detail", args=[s["document"].id]))
    assert response.status_code == 404

def test_revoked_reader_loses_access_after_cached_read(api_client, scenario):
    s = scenario
    grant = Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 200
    authenticate(api_client, s["owner"])
    assert api_client.post(reverse("grant-revoke"), {"grant_id": grant.id}, format="json").status_code == 204
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 404

def test_new_share_takes_effect_after_cached_denial(api_client, scenario):
    s = scenario
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 404
    authenticate(api_client, s["owner"])
    payload = {"document_id": str(s["document"].id), "principal_type": "membership", "principal_id": str(s["reader"].id)}
    assert api_client.post(reverse("grant-create"), payload, format="json").status_code == 201
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 200

def test_revoke_before_first_read_is_enforced(api_client, scenario):
    s = scenario
    grant = Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    authenticate(api_client, s["owner"])
    api_client.post(reverse("grant-revoke"), {"grant_id": grant.id}, format="json")
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 404
