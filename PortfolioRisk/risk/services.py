from decimal import Decimal

from marketdata.services import latest_price, require_fresh
from orders.models import Order


def order_exposure(order, price):
    direction = Decimal("-1") if order.side == Order.Side.SELL else Decimal("1")
    return direction * order.quantity * price


def evaluate_order(order, as_of):
    snapshot = latest_price(order.instrument)
    require_fresh(snapshot, as_of)
    exposure = order_exposure(order, snapshot.price)
    if abs(exposure) > order.portfolio.risk_limit.max_order_notional:
        raise ValueError("order exceeds notional limit")
    return exposure
