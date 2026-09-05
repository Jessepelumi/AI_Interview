from django.db import models

from instruments.models import Instrument
from portfolios.models import Portfolio


class Order(models.Model):
    class Side(models.TextChoices):
        BUY = "B", "BUY"
        SELL = "S", "SELL"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending risk"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.PROTECT, related_name="orders"
    )
    instrument = models.ForeignKey(
        Instrument, on_delete=models.PROTECT, related_name="orders"
    )
    side = models.CharField(max_length=1, choices=Side.choices)
    quantity = models.DecimalField(max_digits=16, decimal_places=4)
    client_order_id = models.CharField(max_length=64)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "client_order_id"],
                name="unique_client_order_per_portfolio",
            )
        ]
