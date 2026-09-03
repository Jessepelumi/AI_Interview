from django.db import models

from catalog.models import Product
from inventory.models import Location


class Order(models.Model):
    order_number = models.CharField(max_length=32, unique=True)
    channel = models.CharField(max_length=24)
    customer_country = models.CharField(max_length=2)
    currency = models.CharField(max_length=3)
    placed_at = models.DateTimeField()

    def __str__(self):
        return self.order_number


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    fulfilment_location = models.ForeignKey(Location, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def paid_total(self):
        return self.unit_price * self.quantity - self.discount_total + self.tax_total
