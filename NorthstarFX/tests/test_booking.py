from datetime import timedelta
from decimal import Decimal
import pytest
from django.utils import timezone
from conversions.services import book_quote
from quotes.services import create_quote
pytestmark = pytest.mark.django_db

def test_booking_is_repeatable_for_same_request(market):
    _, customer = market
    quote = create_quote(customer, "EUR", "USD", Decimal("10.00"))
    first, created = book_quote(quote, "request-1")
    second, repeated = book_quote(quote, "request-1")
    assert created is True and repeated is False and first.id == second.id

def test_expired_quote_is_rejected(market):
    _, customer = market
    quote = create_quote(customer, "EUR", "USD", Decimal("10.00"))
    quote.expires_at = timezone.now() - timedelta(seconds=1); quote.save()
    with pytest.raises(ValueError, match="expired"):
        book_quote(quote, "request-2")
