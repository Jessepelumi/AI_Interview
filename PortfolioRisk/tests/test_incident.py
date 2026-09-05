from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from instruments.models import Instrument
from marketdata.models import PriceSnapshot
from marketdata.provider import MarketDataAdapter
from orders.models import Order
from orders.serializers import OrderCreateSerializer, OrderSerializer
from portfolios.models import Desk, Portfolio
from risk.models import RiskLimit
from risk.services import evaluate_order, order_exposure


class PortfolioRiskIncidentTests(TestCase):
    def setUp(self):
        self.trader = get_user_model().objects.create_user("maya")
        self.outsider = get_user_model().objects.create_user("outsider")
        self.desk = Desk.objects.create(name="Delta One")
        self.desk.members.add(self.trader)
        self.portfolio = Portfolio.objects.create(
            desk=self.desk, name="US Options", base_currency="USD"
        )
        RiskLimit.objects.create(
            portfolio=self.portfolio, max_order_notional=Decimal("1000000.00")
        )
        self.equity = Instrument.objects.create(
            symbol="ACME", asset_type="equity", quote_currency="USD"
        )
        self.option = Instrument.objects.create(
            symbol="ACME-C100",
            asset_type="option",
            quote_currency="USD",
            contract_multiplier=Decimal("100.00"),
        )
        self.now = timezone.now()
        PriceSnapshot.objects.create(
            instrument=self.equity,
            price=Decimal("25.00"),
            observed_at=self.now,
        )
        PriceSnapshot.objects.create(
            instrument=self.option,
            price=Decimal("2.50"),
            observed_at=self.now,
        )

    def test_api_sell_side_is_mapped_to_model_code(self):
        serializer = OrderCreateSerializer(
            data={
                "instrument": "ACME",
                "side": "SELL",
                "quantity": "10.0000",
                "client_order_id": "sell-1",
            },
            context={"portfolio": self.portfolio, "as_of": self.now},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.side, Order.Side.SELL)

    def test_sell_order_has_negative_exposure(self):
        serializer = OrderCreateSerializer(
            data={
                "instrument": "ACME",
                "side": "SELL",
                "quantity": "10.0000",
                "client_order_id": "sell-2",
            },
            context={"portfolio": self.portfolio, "as_of": self.now},
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order_exposure(order, Decimal("25")), Decimal("-250"))

    def test_read_serializer_uses_external_side_vocabulary(self):
        order = Order.objects.create(
            portfolio=self.portfolio,
            instrument=self.equity,
            side=Order.Side.SELL,
            quantity=Decimal("1"),
            client_order_id="sell-read",
        )
        self.assertEqual(OrderSerializer(order).data["side"], "SELL")

    def test_option_notional_includes_contract_multiplier(self):
        order = Order.objects.create(
            portfolio=self.portfolio,
            instrument=self.option,
            side=Order.Side.BUY,
            quantity=Decimal("2"),
            client_order_id="option-1",
        )
        self.assertEqual(order_exposure(order, Decimal("2.50")), Decimal("500.00"))

    def test_price_older_than_five_seconds_is_rejected(self):
        PriceSnapshot.objects.filter(instrument=self.equity).update(
            observed_at=self.now - timedelta(seconds=10)
        )
        order = Order.objects.create(
            portfolio=self.portfolio,
            instrument=self.equity,
            side=Order.Side.BUY,
            quantity=Decimal("1"),
            client_order_id="stale-1",
        )
        with self.assertRaisesMessage(ValueError, "market price is stale"):
            evaluate_order(order, self.now)

    def test_user_cannot_submit_to_another_desks_portfolio(self):
        client = APIClient()
        client.force_authenticate(self.outsider)
        response = client.post(
            f"/api/portfolios/{self.portfolio.id}/orders/",
            {
                "instrument": "ACME",
                "side": "BUY",
                "quantity": "1.0000",
                "client_order_id": "intruder-1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 404)

    def test_fresh_equity_order_uses_plain_notional(self):
        order = Order.objects.create(
            portfolio=self.portfolio,
            instrument=self.equity,
            side=Order.Side.BUY,
            quantity=Decimal("4"),
            client_order_id="buy-1",
        )
        self.assertEqual(evaluate_order(order, self.now), Decimal("100.000000"))

    def test_provider_millisecond_timestamp_is_ingested(self):
        observed = self.now.replace(microsecond=0)
        snapshot = MarketDataAdapter().ingest(
            {
                "symbol": "ACME",
                "price": "26.10",
                "timestamp_ms": int(observed.timestamp() * 1000),
            }
        )
        self.assertEqual(snapshot.observed_at, observed)
