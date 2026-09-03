from django.db import models

from workspaces.models import Workspace


class ChannelConnection(models.Model):
    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="connections"
    )
    channel = models.CharField(max_length=24)
    access_token = models.CharField(max_length=200)
    remote_account_id = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "channel"], name="one_connection_per_channel"
            )
        ]
