from django.conf import settings
from django.db import models


class Workspace(models.Model):
    name = models.CharField(max_length=120)
    timezone_name = models.CharField(max_length=64, default="UTC")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="workspaces")

    def __str__(self):
        return self.name
