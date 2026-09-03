from rest_framework import serializers

from customers.models import Organisation

from .models import Beneficiary


class BeneficiarySerializer(serializers.ModelSerializer):
    organisation_id = serializers.PrimaryKeyRelatedField(
        source="organisation", queryset=Organisation.objects.all()
    )
    account_number = serializers.CharField(source="iban")

    class Meta:
        model = Beneficiary
        fields = (
            "id",
            "organisation_id",
            "name",
            "account_number",
            "bank_country",
        )
        read_only_fields = ("id",)
