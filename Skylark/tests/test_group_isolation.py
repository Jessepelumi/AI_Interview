import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from directory.models import DirectoryGroup, GroupMember
from organizations.models import Membership, Workspace
from sharing.models import Grant
from tests.conftest import authenticate

pytestmark = pytest.mark.django_db

def test_group_grant_allows_member_in_same_workspace(api_client, scenario):
    s = scenario
    group = DirectoryGroup.objects.create(workspace=s["workspace"], external_id="engineering", name="Engineering")
    GroupMember.objects.create(group=group, membership=s["reader"])
    Grant.objects.create(document=s["document"], principal_type="group", principal_id="engineering")
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 200

def test_group_identity_does_not_cross_workspace_boundary(api_client, scenario):
    s = scenario
    other = Workspace.objects.create(slug="beacon", name="Beacon Legal")
    other_membership = Membership.objects.create(workspace=other, user=s["reader"].user)
    other_group = DirectoryGroup.objects.create(workspace=other, external_id="legal", name="Legal")
    GroupMember.objects.create(group=other_group, membership=other_membership)
    atlas_group = DirectoryGroup.objects.create(workspace=s["workspace"], external_id="legal", name="Atlas Legal")
    Grant.objects.create(document=s["document"], principal_type="group", principal_id=atlas_group.external_id)

    authenticate(api_client, other_membership)
    api_client.get(reverse("search"), {"q": "nothing"})  # warms directory subjects
    authenticate(api_client, s["reader"])
    assert api_client.get(reverse("document-detail", args=[s["document"].id])).status_code == 404
