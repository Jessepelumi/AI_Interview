from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=140)
    weight_grams = models.PositiveIntegerField()

    def __str__(self):
        return self.sku
