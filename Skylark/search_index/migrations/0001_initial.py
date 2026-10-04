import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("documents", "0001_initial")]
    operations = [migrations.CreateModel(name="IndexedDocument", fields=[("id", models.BigAutoField(primary_key=True, serialize=False)), ("title", models.CharField(max_length=200)), ("acl_version", models.PositiveIntegerField()), ("allowed_subjects", models.JSONField(default=list)), ("indexed_at", models.DateTimeField(auto_now=True)), ("document", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="search_record", to="documents.document"))])]
