from django.db import transaction
from rest_framework import serializers

from inventory.models import Location
from orders.models import Order, OrderLine

from .models import ReturnLine, ReturnRequest
from .services import calculate_refund, process_return, validate_return_quantity


class ReturnLineInputSerializer(serializers.Serializer):
    order_line_id = serializers.PrimaryKeyRelatedField(
        source="order_line", queryset=OrderLine.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)


class ReturnCreateSerializer(serializers.Serializer):
    order_id = serializers.PrimaryKeyRelatedField(source="order", queryset=Order.objects.all())
    receiving_location = serializers.SlugRelatedField(
        slug_field="code", queryset=Location.objects.all()
    )
    reason = serializers.ChoiceField(choices=ReturnRequest.Reason.choices)
    lines = ReturnLineInputSerializer(many=True)

    @transaction.atomic
    def create(self, validated_data):
        lines = validated_data.pop("lines")
        return_request = ReturnRequest.objects.create(**validated_data)
        for item in lines:
            order_line = item["order_line"]
            units = item["quantity"]
            if order_line.order_id != return_request.order_id:
                raise serializers.ValidationError("line does not belong to order")
            validate_return_quantity(order_line, units)
            ReturnLine.objects.create(
                return_request=return_request,
                order_line=order_line,
                units=units,
                refund_amount=calculate_refund(order_line, units),
            )
        return process_return(return_request)


class ReturnSerializer(serializers.ModelSerializer):
    reason_code = serializers.CharField(source="reason")
    receiving_location = serializers.SlugRelatedField(read_only=True, slug_field="code")

    class Meta:
        model = ReturnRequest
        fields = ("id", "order_id", "receiving_location", "reason_code", "status")
