from datetime import UTC, datetime
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from catalog.models import Product
from inventory.models import Location, StockLevel
from orders.models import Order, OrderLine
from returns.models import ReturnLine, ReturnRequest
from returns.services import calculate_refund, process_return, validate_return_quantity
from shipping.services import build_label_payload, select_carrier


class OmnichannelReturnIncidentTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            sku="COAT-GRN-M", name="Green coat", weight_grams=750
        )
        self.belfast = Location.objects.create(
            code="BFS-WH", name="Belfast Warehouse", country_code="GB", kind="warehouse"
        )
        self.dublin = Location.objects.create(
            code="DUB-01", name="Dublin Grafton", country_code="IE", kind="store"
        )
        self.order = Order.objects.create(
            order_number="WEB-1001",
            channel="web",
            customer_country="IE",
            currency="EUR",
            placed_at=datetime(2026, 8, 1, 12, tzinfo=UTC),
        )
        self.line = OrderLine.objects.create(
            order=self.order,
            product=self.product,
            fulfilment_location=self.belfast,
            quantity=3,
            unit_price=Decimal("20.00"),
            discount_total=Decimal("10.00"),
            tax_total=Decimal("11.50"),
        )

    def make_return(self, units=2):
        request = ReturnRequest.objects.create(
            order=self.order,
            receiving_location=self.dublin,
            reason=ReturnRequest.Reason.UNWANTED,
        )
        ReturnLine.objects.create(
            return_request=request,
            order_line=self.line,
            units=units,
            refund_amount=calculate_refund(self.line, units),
        )
        return request

    def test_api_accepts_documented_reason_code(self):
        response = APIClient().post(
            "/api/returns/",
            {
                "order_id": self.order.id,
                "receiving_location": "DUB-01",
                "reason_code": "unwanted",
                "lines": [{"order_line_id": self.line.id, "quantity": 1}],
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["reason_code"], "unwanted")

    def test_partial_refund_prorates_actual_paid_total(self):
        # Paid total is 60 - 10 + 11.50 = 61.50; two of three units = 41.00.
        self.assertEqual(calculate_refund(self.line, 2), Decimal("41.00"))

    def test_store_return_restock_goes_to_receiving_store(self):
        request = self.make_return(units=2)
        process_return(request)
        self.assertTrue(
            StockLevel.objects.filter(location=self.dublin, product=self.product).exists()
        )
        dublin_stock = StockLevel.objects.get(location=self.dublin, product=self.product)
        self.assertEqual(dublin_stock.on_hand, 2)
        self.assertFalse(
            StockLevel.objects.filter(location=self.belfast, product=self.product).exists()
        )

    def test_label_converts_grams_to_kilograms(self):
        request = self.make_return(units=2)
        self.assertEqual(build_label_payload(request)["weight_kg"], "1.500")

    def test_irish_store_selects_an_post_configuration(self):
        request = self.make_return(units=1)
        self.assertEqual(select_carrier(request), "anpost")

    def test_cannot_return_more_than_was_purchased(self):
        request = self.make_return(units=2)
        with self.assertRaisesMessage(ValueError, "exceeds purchased"):
            validate_return_quantity(self.line, 2)
        self.assertEqual(request.lines.count(), 1)

    def test_processing_is_idempotent(self):
        request = self.make_return(units=1)
        process_return(request)
        process_return(request)
        self.assertTrue(
            StockLevel.objects.filter(location=self.dublin, product=self.product).exists()
        )
        stock = StockLevel.objects.get(location=self.dublin, product=self.product)
        self.assertEqual(stock.on_hand, 1)

    def test_return_line_preserves_catalogue_product(self):
        request = self.make_return(units=1)
        self.assertEqual(request.lines.get().order_line.product.sku, "COAT-GRN-M")
