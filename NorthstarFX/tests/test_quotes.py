from decimal import Decimal
import pytest
from django.core.cache import cache
from quotes.services import create_quote
pytestmark = pytest.mark.django_db

def test_quote_calculates_buy_amount(market):
    _, customer = market
    quote = create_quote(customer, "EUR", "USD", Decimal("100.00"))
    assert quote.buy_amount == Decimal("110.00")

def test_currency_pairs_do_not_share_cached_rate(market):
    _, customer = market
    cache.clear()
    usd = create_quote(customer, "EUR", "USD", Decimal("100.00"))
    gbp = create_quote(customer, "EUR", "GBP", Decimal("100.00"))
    assert usd.rate != gbp.rate

def test_inverse_pair_uses_reciprocal(market):
    _, customer = market
    cache.clear()
    quote = create_quote(customer, "USD", "EUR", Decimal("110.00"))
    assert quote.buy_amount == Decimal("100.00")
