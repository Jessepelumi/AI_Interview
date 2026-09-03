from django.conf import settings
from django.db import models
class Customer(models.Model):
    name = models.CharField(max_length=160)
    external_id = models.CharField(max_length=80, unique=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="fx_customers")
    markup_bps = models.PositiveIntegerField(default=25)
