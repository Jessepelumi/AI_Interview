from django.conf import settings
from django.db import models

from workspaces.models import Workspace


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        SCHEDULED = "scheduled", "Scheduled"
        PUBLISHED = "published", "Published"

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="posts"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    body = models.TextField()
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.DRAFT
    )
    scheduled_for = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:40]
