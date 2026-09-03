from datetime import UTC, datetime
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from accounts.models import Account
from beneficiaries.models import Beneficiary
from customers.models import Organisation
from integrations.gateway import ClearingGateway
from transfers.services import calculate_fee, create_transfer, next_settlement_date


class DublinTransferIncidentTests(TestCase):
    def setUp(self):
        self.organisation = Organisation.objects.create(
            legal_name="Liffey Design Ltd",
            country_code="IE",
            timezone_name="Europe/Dublin",
        )
        self.account = Account.objects.create(
            organisation=self.organisation,
            currency="EUR",
            available_balance=Decimal("5000.00"),
        )
        self.beneficiary = Beneficiary.objects.create(
            organisation=self.organisation,
            name="Paper Supplies",
            iban="IE29 AIBK 9311 5212 3456 78",
            bank_country="IE",
        )

    def test_documented_beneficiary_iban_is_accepted_by_api(self):
        response = APIClient().post(
            "/api/beneficiaries/",
            {
                "organisation_id": self.organisation.id,
                "name": "Printer Repairs",
                "iban": "IE64IRCE92050112345678",
                "bank_country": "IE",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["iban"], "IE64IRCE92050112345678")

    def test_irish_fee_configuration_is_applied(self):
        self.assertEqual(
            calculate_fee(self.account, Decimal("1000.00")), Decimal("1.50")
        )

    def test_dublin_request_after_local_cutoff_moves_to_next_business_day(self):
        # 16:30 UTC is 17:30 in Dublin during Irish summer time.
        requested_at = datetime(2026, 7, 6, 16, 30, tzinfo=UTC)

        self.assertEqual(
            next_settlement_date(self.account, requested_at).isoformat(), "2026-07-07"
        )

    def test_same_reference_is_scoped_to_account(self):
        second_account = Account.objects.create(
            organisation=self.organisation,
            currency="EUR",
            available_balance=Decimal("9000.00"),
        )
        first, _ = create_transfer(
            self.account, self.beneficiary, Decimal("10.00"), "mobile-101"
        )
        second, created = create_transfer(
            second_account, self.beneficiary, Decimal("20.00"), "mobile-101"
        )

        self.assertTrue(created)
        self.assertNotEqual(first.id, second.id)
        self.assertEqual(second.account, second_account)

    def test_same_account_retry_is_idempotent(self):
        first, created = create_transfer(
            self.account, self.beneficiary, Decimal("10.00"), "retry-7"
        )
        second, repeated = create_transfer(
            self.account, self.beneficiary, Decimal("10.00"), "retry-7"
        )

        self.assertTrue(created)
        self.assertFalse(repeated)
        self.assertEqual(first.id, second.id)

    def test_friday_after_cutoff_skips_weekend(self):
        # January is UTC in Dublin, so this is unambiguously after cutoff.
        requested_at = datetime(2026, 1, 9, 18, 0, tzinfo=UTC)
        self.assertEqual(
            next_settlement_date(self.account, requested_at).isoformat(), "2026-01-12"
        )

    def test_clearing_payload_normalises_iban(self):
        transfer, _ = create_transfer(
            self.account, self.beneficiary, Decimal("12.34"), "gateway-5"
        )
        payload = ClearingGateway.build_payload(transfer)
        self.assertEqual(payload["creditor_iban"], "IE29AIBK93115212345678")
        self.assertEqual(payload["currency"], "EUR")
