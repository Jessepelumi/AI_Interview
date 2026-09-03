from django.db import models

from inventory.models import Location
from orders.models import Order, OrderLine


class ReturnRequest(models.Model):
    class Reason(models.TextChoices):
        DAMAGED = "damaged", "Damaged"
        UNWANTED = "unwanted", "Unwanted"
        WRONG_ITEM = "wrong_item", "Wrong item"

    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        COMPLETED = "completed", "Completed"

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="returns")
    receiving_location = models.ForeignKey(Location, on_delete=models.PROTECT)
    reason = models.CharField(max_length=20, choices=Reason.choices)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.REQUESTED
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ReturnLine(models.Model):
    return_request = models.ForeignKey(
        ReturnRequest, on_delete=models.CASCADE, related_name="lines"
    )
    order_line = models.ForeignKey(OrderLine, on_delete=models.PROTECT, related_name="return_lines")
    units = models.PositiveSmallIntegerField()
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2)
