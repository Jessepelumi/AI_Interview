import django.db.models.deletion
import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("documents", "0001_initial"), ("organizations", "0001_initial")]
    operations = [migrations.CreateModel(name="ExportJob", fields=[("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)), ("status", models.CharField(choices=[("queued", "Queued"), ("complete", "Complete"), ("denied", "Denied")], default="queued", max_length=16)), ("artifact_key", models.CharField(blank=True, max_length=255)), ("created_at", models.DateTimeField(auto_now_add=True)), ("completed_at", models.DateTimeField(blank=True, null=True)), ("document", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="documents.document")), ("requested_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.membership"))])]
