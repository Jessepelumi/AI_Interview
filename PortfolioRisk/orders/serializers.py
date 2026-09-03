from decimal import Decimal

from django.utils import timezone
from rest_framework import serializers

from instruments.models import Instrument

from .models import Order
from .services import submit_order


class OrderCreateSerializer(serializers.Serializer):
    instrument = serializers.SlugRelatedField(
        slug_field="symbol", queryset=Instrument.objects.all()
    )
    side = serializers.ChoiceField(choices=("BUY", "SELL"))
    quantity = serializers.DecimalField(
        max_digits=16, decimal_places=4, min_value=Decimal("0.0001")
    )
    client_order_id = serializers.CharField(max_length=64)

    def create(self, validated_data):
        order, _ = submit_order(
            portfolio=self.context["portfolio"],
            as_of=self.context.get("as_of", timezone.now()),
            **validated_data,
        )
        return order


class OrderSerializer(serializers.ModelSerializer):
    instrument = serializers.SlugRelatedField(read_only=True, slug_field="symbol")

    class Meta:
        model = Order
        fields = ("id", "instrument", "side", "quantity", "client_order_id", "status")
