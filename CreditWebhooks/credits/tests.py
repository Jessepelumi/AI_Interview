import json
from decimal import Decimal

from django.test import TestCase

from .models import Account, WebhookEvent
from .services import apply_provider_event


def credit_payload(event_id="evt_100", account_id="acct_1", amount_minor=1299):
    return {
        "id": event_id,
        "type": "credit.applied",
        "data": {"account_id": account_id, "amount_minor": amount_minor},
    }


class ProviderEventServiceTests(TestCase):
    def test_minor_units_are_converted_to_major_units(self):
        account = Account.objects.create(
            external_id="acct_1", balance=Decimal("5.00")
        )

        result = apply_provider_event(credit_payload())

        account.refresh_from_db()
        self.assertTrue(result.applied)
        self.assertEqual(account.balance, Decimal("17.99"))

    def test_duplicate_delivery_is_applied_once(self):
        account = Account.objects.create(
            external_id="acct_1", balance=Decimal("0.00")
        )
        payload = credit_payload(amount_minor=250)

        first = apply_provider_event(payload)
        second = apply_provider_event(payload)

        account.refresh_from_db()
        self.assertTrue(first.applied)
        self.assertFalse(second.applied)
        self.assertEqual(second.reason, "duplicate")
        self.assertEqual(account.balance, Decimal("2.50"))
        self.assertEqual(WebhookEvent.objects.count(), 1)

    def test_failed_processing_rolls_back_event_so_retry_can_succeed(self):
        payload = credit_payload(
            event_id="evt_retry", account_id="acct_late", amount_minor=500
        )

        with self.assertRaises(Account.DoesNotExist):
            apply_provider_event(payload)
        self.assertFalse(
            WebhookEvent.objects.filter(provider_event_id="evt_retry").exists()
        )

        account = Account.objects.create(
            external_id="acct_late", balance=Decimal("0.00")
        )
        retried = apply_provider_event(payload)

        account.refresh_from_db()
        self.assertTrue(retried.applied)
        self.assertEqual(account.balance, Decimal("5.00"))

    def test_successful_event_is_marked_processed(self):
        Account.objects.create(external_id="acct_1")

        apply_provider_event(credit_payload(amount_minor=100))

        event = WebhookEvent.objects.get(provider_event_id="evt_100")
        self.assertIsNotNone(event.processed_at)


class ProviderWebhookApiTests(TestCase):
    def test_ignored_event_returns_stable_response(self):
        payload = {"id": "evt_other", "type": "account.updated", "data": {}}

        response = self.client.post(
            "/api/webhooks/provider/",
            data=json.dumps(payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"applied": False, "reason": "ignored"}
        )
