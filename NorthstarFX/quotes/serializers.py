from rest_framework import serializers
from .models import Quote
from .services import create_quote
class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["id", "customer", "sell_currency", "buy_currency", "sell_amount", "buy_amount", "rate", "expires_at", "created_at"]
        read_only_fields = ["id", "buy_amount", "rate", "expires_at", "created_at"]
    def create(self, validated_data):
        return create_quote(**validated_data)
