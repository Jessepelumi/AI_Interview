from django.db import models

from portfolios.models import Portfolio


class RiskLimit(models.Model):
    portfolio = models.OneToOneField(
        Portfolio, on_delete=models.CASCADE, related_name="risk_limit"
    )
    max_order_notional = models.DecimalField(max_digits=20, decimal_places=2)
