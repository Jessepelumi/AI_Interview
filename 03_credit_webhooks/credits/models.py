from django.db import models


class Account(models.Model):
    external_id = models.CharField(max_length=64, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.external_id


class WebhookEvent(models.Model):
    provider_event_id = models.CharField(max_length=80, unique=True)
    event_type = models.CharField(max_length=40)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.provider_event_id

