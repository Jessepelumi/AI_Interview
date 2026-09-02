from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sku}: {self.name}"


class Coupon(models.Model):
    code = models.CharField(max_length=32, unique=True)
    percent_discount = models.PositiveSmallIntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

