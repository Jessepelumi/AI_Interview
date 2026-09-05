from rest_framework import serializers
from .models import Dispute, Evidence
from .services import validate_amount

class EvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = ["id", "filename", "storage_key", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]

class DisputeSerializer(serializers.ModelSerializer):
    evidence = EvidenceSerializer(many=True, read_only=True)
    payment_reference = serializers.CharField(source="payment.processor_reference", read_only=True)
    class Meta:
        model = Dispute
        fields = ["id", "organisation", "payment", "payment_reference", "reason", "amount", "state",
                  "response_due_at", "evidence", "created_at", "updated_at"]
        read_only_fields = ["state", "created_at", "updated_at"]
    def validate(self, attrs):
        payment = attrs.get("payment") or getattr(self.instance, "payment", None)
        amount = attrs.get("amount") or getattr(self.instance, "amount", None)
        if payment and amount:
            validate_amount(payment, amount)
        return attrs
