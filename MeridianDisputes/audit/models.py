from django.conf import settings
from django.db import models

class AuditEvent(models.Model):
    dispute_id = models.PositiveBigIntegerField(db_index=True)
    action = models.CharField(max_length=80)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
