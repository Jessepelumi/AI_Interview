from django.db import models

from returns.models import ReturnRequest


class ReturnShipment(models.Model):
    return_request = models.OneToOneField(
        ReturnRequest, on_delete=models.CASCADE, related_name="shipment"
    )
    carrier = models.CharField(max_length=24)
    label_id = models.CharField(max_length=100)
