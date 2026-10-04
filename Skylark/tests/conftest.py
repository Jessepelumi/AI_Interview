import pytest
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APIClient
from documents.models import Document
from organizations.models import Membership, Workspace

@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def scenario(db):
    User = get_user_model()
    owner_user = User.objects.create_user("owner", email="owner@example.test")
    reader_user = User.objects.create_user("reader", email="reader@example.test")
    outsider_user = User.objects.create_user("outsider", email="outsider@example.test")
    workspace = Workspace.objects.create(slug="atlas", name="Atlas Research")
    owner = Membership.objects.create(workspace=workspace, user=owner_user, role="admin")
    reader = Membership.objects.create(workspace=workspace, user=reader_user)
    outsider = Membership.objects.create(workspace=workspace, user=outsider_user)
    document = Document.objects.create(workspace=workspace, owner=owner, title="Project Aurora", body="Restricted launch plan")
    return {"workspace": workspace, "owner": owner, "reader": reader, "outsider": outsider, "document": document}

def authenticate(client, membership):
    client.credentials(HTTP_X_USER_ID=str(membership.user_id), HTTP_X_WORKSPACE=membership.workspace.slug)
