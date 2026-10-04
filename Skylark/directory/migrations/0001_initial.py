import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("organizations", "0001_initial")]
    operations = [
        migrations.CreateModel(name="DirectoryGroup", fields=[("id", models.BigAutoField(primary_key=True, serialize=False)), ("external_id", models.CharField(max_length=80)), ("name", models.CharField(max_length=120)), ("workspace", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.workspace"))], options={"constraints": [models.UniqueConstraint(fields=("workspace", "external_id"), name="uniq_workspace_group_external_id")]}),
        migrations.CreateModel(name="GroupMember", fields=[("id", models.BigAutoField(primary_key=True, serialize=False)), ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="directory.directorygroup")), ("membership", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="group_links", to="organizations.membership"))], options={"constraints": [models.UniqueConstraint(fields=("group", "membership"), name="uniq_group_membership")]}),
    ]
