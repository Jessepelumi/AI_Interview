from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.utils import timezone

from .models import Transfer

PENNY = Decimal("0.01")


def calculate_fee(account, amount):
    country = account.organisation.country_code.lower()
    basis_points = settings.BANK_FEE_BPS_BY_COUNTRY.get(
        country, settings.BANK_FEE_BPS_BY_COUNTRY["DEFAULT"]
    )
    return (amount * Decimal(basis_points) / Decimal("10000")).quantize(
        PENNY, rounding=ROUND_HALF_UP
    )


def next_settlement_date(account, requested_at):
    local_request = timezone.localtime(requested_at)
    day = local_request.date()
    if local_request.hour >= settings.TRANSFER_CUTOFF_HOUR:
        day += timedelta(days=1)
    while day.weekday() >= 5:
        day += timedelta(days=1)
    return day


def create_transfer(account, beneficiary, amount, client_reference, requested_at=None):
    if beneficiary.organisation_id != account.organisation_id:
        raise ValueError("beneficiary is not owned by this organisation")

    requested_at = requested_at or timezone.now()
    transfer, created = Transfer.objects.get_or_create(
        client_reference=client_reference,
        defaults={
            "account": account,
            "beneficiary": beneficiary,
            "amount": amount,
            "fee": calculate_fee(account, amount),
            "requested_at": requested_at,
            "settlement_date": next_settlement_date(account, requested_at),
        },
    )
    return transfer, created
