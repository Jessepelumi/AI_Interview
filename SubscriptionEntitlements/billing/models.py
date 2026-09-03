from django.db import models

from customers.models import Customer
from plans.models import Plan


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAST_DUE = "past_due", "Past due"
        CANCELLED = "cancelled", "Cancelled"

    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    external_reference = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=16, choices=Status.choices)
    ends_on = models.DateField(null=True, blank=True)


class BillingEvent(models.Model):
    provider = models.CharField(max_length=24)
    external_event_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=40)
    processed_at = models.DateTimeField(null=True, blank=True)


class Payment(models.Model):
    event = models.OneToOneField(BillingEvent, on_delete=models.PROTECT)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.PROTECT, related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
