from django.conf import settings
from django.db import models
from accounts.models import Organisation
from payments.models import Payment

class Dispute(models.Model):
    class State(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        EVIDENCE_REQUIRED = "evidence_required", "Evidence required"
        WON = "won", "Won"
        LOST = "lost", "Lost"
        CLOSED = "closed", "Closed"
    organisation = models.ForeignKey(Organisation, on_delete=models.PROTECT)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="disputes")
    reason = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    state = models.CharField(max_length=30, choices=State.choices, default=State.DRAFT)
    response_due_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Evidence(models.Model):
    dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name="evidence")
    filename = models.CharField(max_length=255)
    storage_key = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ProcessorEvent(models.Model):
    event_id = models.CharField(max_length=100)
    dispute = models.ForeignKey(Dispute, on_delete=models.CASCADE, related_name="processor_events")
    event_type = models.CharField(max_length=80)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)
