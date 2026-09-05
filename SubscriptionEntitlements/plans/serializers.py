from rest_framework import serializers

from .models import Plan, PlanFeature


class PlanFeatureSerializer(serializers.ModelSerializer):
    feature_code = serializers.CharField(source="feature.code")

    class Meta:
        model = PlanFeature
        fields = ("feature_code", "enabled", "limit")


class PlanSerializer(serializers.ModelSerializer):
    features = PlanFeatureSerializer(source="feature_rules", many=True)

    class Meta:
        model = Plan
        fields = ("slug", "name", "active", "features")
