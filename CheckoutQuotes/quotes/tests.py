import json
from decimal import Decimal

from django.test import TestCase

from .models import Coupon, Product
from .services import build_quote


class QuoteServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            sku="WIDGET", name="Desk widget", unit_price=Decimal("12.50")
        )
        Product.objects.create(
            sku="CABLE", name="Cable", unit_price=Decimal("3.00")
        )
        Product.objects.create(
            sku="SAMPLE", name="Sample", unit_price=Decimal("0.05")
        )
        Coupon.objects.create(code="SAVE10", percent_discount=10, active=True)
        Coupon.objects.create(code="OLD10", percent_discount=10, active=False)

    def test_subtotal_uses_each_line_quantity(self):
        quote = build_quote(
            [
                {"sku": "WIDGET", "quantity": 2},
                {"sku": "CABLE", "quantity": 3},
            ]
        )

        self.assertEqual(quote.subtotal, Decimal("34.00"))
        self.assertEqual(quote.total, Decimal("34.00"))

    def test_percentage_discount_rounds_half_up(self):
        quote = build_quote(
            [{"sku": "SAMPLE", "quantity": 1}], coupon_code="SAVE10"
        )

        self.assertEqual(quote.discount, Decimal("0.01"))
        self.assertEqual(quote.total, Decimal("0.04"))

    def test_inactive_coupon_has_no_effect(self):
        quote = build_quote(
            [{"sku": "WIDGET", "quantity": 1}], coupon_code="OLD10"
        )

        self.assertEqual(quote.discount, Decimal("0.00"))
        self.assertEqual(quote.total, Decimal("12.50"))


class QuoteApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            sku="MUG", name="Coffee mug", unit_price=Decimal("8.25")
        )

    def test_quote_endpoint_returns_string_formatted_money(self):
        response = self.client.post(
            "/api/quotes/",
            data=json.dumps({"items": [{"sku": "MUG", "quantity": 2}]}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"subtotal": "16.50", "discount": "0.00", "total": "16.50"},
        )

