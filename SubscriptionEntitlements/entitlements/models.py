from django.db import models

from customers.models import Customer
from plans.models import Feature


class UsageCounter(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    period = models.DateField()
    used = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "feature", "period"], name="unique_usage_period"
            )
        ]
