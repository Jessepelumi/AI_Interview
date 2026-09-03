from decimal import Decimal

from rest_framework import serializers

from beneficiaries.models import Beneficiary

from .models import Transfer
from .services import create_transfer


class TransferCreateSerializer(serializers.Serializer):
    beneficiary_id = serializers.PrimaryKeyRelatedField(
        source="beneficiary", queryset=Beneficiary.objects.all()
    )
    amount = serializers.DecimalField(
        max_digits=14, decimal_places=2, min_value=Decimal("0.01")
    )
    client_reference = serializers.CharField(max_length=64)

    def create(self, validated_data):
        transfer, _ = create_transfer(
            account=self.context["account"], **validated_data
        )
        return transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = (
            "id",
            "client_reference",
            "amount",
            "fee",
            "settlement_date",
            "status",
        )
