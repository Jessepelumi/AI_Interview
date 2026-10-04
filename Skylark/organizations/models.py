from django.conf import settings
from django.db import models

class Workspace(models.Model):
    id = models.BigAutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)

class Membership(models.Model):
    id = models.BigAutoField(primary_key=True)
    class Role(models.TextChoices):
        MEMBER = "member"
        ADMIN = "admin"

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.MEMBER)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["workspace", "user"], name="uniq_workspace_user")]

    @property
    def is_authenticated(self):
        return True
