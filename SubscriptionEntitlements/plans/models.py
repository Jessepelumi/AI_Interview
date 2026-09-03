from django.db import models


class Feature(models.Model):
    code = models.SlugField(unique=True)
    description = models.CharField(max_length=160)

    def __str__(self):
        return self.code


class Plan(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    features = models.ManyToManyField(Feature, through="PlanFeature")

    def __str__(self):
        return self.name


class PlanFeature(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="feature_rules")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    limit = models.PositiveIntegerField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "feature"], name="unique_feature_per_plan"
            )
        ]
