from django.db import models


class Organisation(models.Model):
    legal_name = models.CharField(max_length=160)
    country_code = models.CharField(max_length=2)
    timezone_name = models.CharField(max_length=64, default="Europe/Dublin")

    def __str__(self):
        return self.legal_name
