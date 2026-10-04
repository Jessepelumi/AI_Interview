from django.db import models
from documents.models import Document

class IndexedDocument(models.Model):
    id = models.BigAutoField(primary_key=True)
    document = models.OneToOneField(Document, on_delete=models.CASCADE, related_name="search_record")
    title = models.CharField(max_length=200)
    acl_version = models.PositiveIntegerField()
    allowed_subjects = models.JSONField(default=list)
    indexed_at = models.DateTimeField(auto_now=True)
