from django.db import models

from catalog.models import Product


class Location(models.Model):
    class Kind(models.TextChoices):
        STORE = "store", "Store"
        WAREHOUSE = "warehouse", "Warehouse"

    code = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    kind = models.CharField(max_length=12, choices=Kind.choices)

    def __str__(self):
        return self.code


class StockLevel(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="stock")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock")
    on_hand = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["location", "product"], name="unique_stock_location_product"
            )
        ]
