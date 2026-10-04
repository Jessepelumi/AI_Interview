from django.db import models
from organizations.models import Membership, Workspace

class DirectoryGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    external_id = models.CharField(max_length=80)
    name = models.CharField(max_length=120)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["workspace", "external_id"], name="uniq_workspace_group_external_id")]

class GroupMember(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(DirectoryGroup, on_delete=models.CASCADE, related_name="memberships")
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="group_links")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["group", "membership"], name="uniq_group_membership")]
