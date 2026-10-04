import pytest
from django.urls import reverse
from exports.models import ExportJob
from exports.services import execute_export
from sharing.models import Grant
from sharing.services import revoke_grant
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db

def test_authorized_export_completes(api_client, scenario):
    s = scenario
    Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    authenticate(api_client, s["reader"])
    response = api_client.post(reverse("export-create", args=[s["document"].id]))
    job = execute_export(response.data["id"])
    assert job.status == ExportJob.Status.COMPLETE
    assert job.artifact_key.endswith(".pdf")

def test_queued_export_is_denied_if_access_is_revoked_before_execution(api_client, scenario):
    s = scenario
    grant = Grant.objects.create(document=s["document"], principal_type="membership", principal_id=str(s["reader"].id))
    authenticate(api_client, s["reader"])
    response = api_client.post(reverse("export-create", args=[s["document"].id]))
    revoke_grant(grant)
    job = execute_export(response.data["id"])
    assert job.status == ExportJob.Status.DENIED
    assert job.artifact_key == ""
