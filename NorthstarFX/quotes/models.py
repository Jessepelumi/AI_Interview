import uuid
from django.db import models
from customers.models import Customer
class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="quotes")
    sell_currency = models.CharField(max_length=3)
    buy_currency = models.CharField(max_length=3)
    sell_amount = models.DecimalField(max_digits=18, decimal_places=2)
    buy_amount = models.DecimalField(max_digits=18, decimal_places=2)
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
