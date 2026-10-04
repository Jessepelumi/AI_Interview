import uuid
from django.db import models
from organizations.models import Membership, Workspace

class Document(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active"
        DELETED = "deleted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    owner = models.ForeignKey(Membership, on_delete=models.PROTECT, related_name="owned_documents")
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    content_version = models.PositiveIntegerField(default=1)
    acl_version = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
