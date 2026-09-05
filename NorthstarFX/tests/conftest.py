from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from customers.models import Customer
from marketdata.models import MarketRate
@pytest.fixture
def market(db):
    user = get_user_model().objects.create_user("trader", password="password")
    customer = Customer.objects.create(name="Acme Imports", external_id="cust_1", markup_bps=0)
    customer.users.add(user)
    MarketRate.objects.create(base_currency="EUR", quote_currency="USD", rate=Decimal("1.1000000000"), observed_at=timezone.now())
    MarketRate.objects.create(base_currency="EUR", quote_currency="GBP", rate=Decimal("0.8500000000"), observed_at=timezone.now())
    return user, customer
