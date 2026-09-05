import uuid
from django.db import models
from quotes.models import Quote
class Conversion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quote = models.ForeignKey(Quote, on_delete=models.PROTECT, related_name="conversions")
    idempotency_key = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="booked")
    booked_at = models.DateTimeField(auto_now_add=True)
