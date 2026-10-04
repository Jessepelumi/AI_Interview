import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]
    operations = [
        migrations.CreateModel(name="Workspace", fields=[("id", models.BigAutoField(primary_key=True, serialize=False)), ("slug", models.SlugField(unique=True)), ("name", models.CharField(max_length=120))]),
        migrations.CreateModel(name="Membership", fields=[("id", models.BigAutoField(primary_key=True, serialize=False)), ("role", models.CharField(choices=[("member", "Member"), ("admin", "Admin")], default="member", max_length=16)), ("active", models.BooleanField(default=True)), ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)), ("workspace", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="organizations.workspace"))], options={"constraints": [models.UniqueConstraint(fields=("workspace", "user"), name="uniq_workspace_user")]}),
    ]
