import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("documents", "0001_initial")]
    operations = [migrations.CreateModel(name="Grant", fields=[("id", models.BigAutoField(primary_key=True, serialize=False)), ("principal_type", models.CharField(choices=[("membership", "Membership"), ("group", "Group")], max_length=16)), ("principal_id", models.CharField(max_length=80)), ("active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("document", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="grants", to="documents.document"))], options={"constraints": [models.UniqueConstraint(fields=("document", "principal_type", "principal_id"), name="uniq_document_principal")]})]
