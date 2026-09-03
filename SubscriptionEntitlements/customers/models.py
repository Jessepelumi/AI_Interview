from django.db import models


class Customer(models.Model):
    external_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    country_code = models.CharField(max_length=2)
    timezone_name = models.CharField(max_length=64, default="UTC")

    def __str__(self):
        return self.name
