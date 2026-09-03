from django.conf import settings
from django.db import models


class Desk(models.Model):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="desks")

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=80)
    base_currency = models.CharField(max_length=3, default="USD")

    def __str__(self):
        return self.name
