from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from customers.models import Customer
from marketdata.models import MarketRate
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user, _ = get_user_model().objects.get_or_create(username="trader")
        customer, _ = Customer.objects.get_or_create(external_id="cust_demo", defaults={"name": "Demo Imports", "markup_bps": 25})
        customer.users.add(user)
        for base, quote, rate in [("GBP", "USD", "1.2750000000"), ("EUR", "USD", "1.0900000000"), ("EUR", "GBP", "0.8550000000")]:
            MarketRate.objects.get_or_create(base_currency=base, quote_currency=quote, provider="primary",
                defaults={"rate": Decimal(rate), "observed_at": timezone.now()})
        self.stdout.write(self.style.SUCCESS("Demo market data ready; user: trader"))
