from django.conf import settings
from django.db import models

class Organisation(models.Model):
    name = models.CharField(max_length=160)
    processor_account_id = models.CharField(max_length=80, unique=True)

class Membership(models.Model):
    class Role(models.TextChoices):
        AGENT = "agent", "Agent"
        MANAGER = "manager", "Manager"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "organisation"], name="unique_org_membership")]
