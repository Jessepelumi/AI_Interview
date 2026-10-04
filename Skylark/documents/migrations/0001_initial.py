import django.db.models.deletion
import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("organizations", "0001_initial")]
    operations = [migrations.CreateModel(name="Document", fields=[("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)), ("title", models.CharField(max_length=200)), ("body", models.TextField(blank=True)), ("status", models.CharField(choices=[("active", "Active"), ("deleted", "Deleted")], default="active", max_length=16)), ("content_version", models.PositiveIntegerField(default=1)), ("acl_version", models.PositiveIntegerField(default=1)), ("updated_at", models.DateTimeField(auto_now=True)), ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="owned_documents", to="organizations.membership")), ("workspace", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.workspace"))])]
