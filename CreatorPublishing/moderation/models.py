from django.db import models

from content.models import Post


class ModerationDecision(models.Model):
    class Outcome(models.TextChoices):
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        REVIEW = "review", "Manual review"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="decisions")
    provider_result = models.CharField(max_length=24)
    outcome = models.CharField(max_length=16, choices=Outcome.choices)
    created_at = models.DateTimeField(auto_now_add=True)
