import uuid
from django.db import models
from documents.models import Document
from organizations.models import Membership

class ExportJob(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued"
        COMPLETE = "complete"
        DENIED = "denied"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(Membership, on_delete=models.CASCADE)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.QUEUED)
    artifact_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
