from django.db import models
from documents.models import Document

class Grant(models.Model):
    id = models.BigAutoField(primary_key=True)
    class PrincipalType(models.TextChoices):
        MEMBERSHIP = "membership"
        GROUP = "group"

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="grants")
    principal_type = models.CharField(max_length=16, choices=PrincipalType.choices)
    principal_id = models.CharField(max_length=80)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["document", "principal_type", "principal_id"], name="uniq_document_principal")]
