import json
from datetime import UTC, date, datetime
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from billing.models import BillingEvent, Payment, Subscription
from billing.services import apply_invoice_paid
from customers.models import Customer
from entitlements.services import feature_limit, has_feature_access
from integrations.signatures import expected_signature
from plans.models import Feature, Plan, PlanFeature


def paid_payload(event_id, subscription_id, amount_minor=1299):
    return {
        "id": event_id,
        "type": "invoice.paid",
        "data": {
            "subscription_id": subscription_id,
            "amount_minor": amount_minor,
            "currency": "EUR",
        },
    }


class SubscriptionEntitlementIncidentTests(TestCase):
    def setUp(self):
        self.exports = Feature.objects.create(code="exports", description="CSV exports")
        self.plan = Plan.objects.create(slug="growth", name="Growth")
        PlanFeature.objects.create(
            plan=self.plan, feature=self.exports, enabled=True, limit=50
        )
        self.customer = Customer.objects.create(
            external_id="cus_ie_1",
            name="Dublin Analytics",
            country_code="IE",
            timezone_name="Europe/Dublin",
        )
        self.subscription = Subscription.objects.create(
            customer=self.customer,
            plan=self.plan,
            external_reference="sub_ie_1",
            status=Subscription.Status.PAST_DUE,
        )

    def test_plan_api_uses_documented_feature_key(self):
        response = APIClient().get("/api/plans/growth/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["features"],
            [{"key": "exports", "enabled": True, "limit": 50}],
        )

    def test_webhook_accepts_documented_signature_header(self):
        body = json.dumps(
            paid_payload("evt_header", self.subscription.external_reference),
            separators=(",", ":"),
        ).encode()
        response = APIClient().generic(
            "POST",
            "/webhooks/billing/stripe/",
            data=body,
            content_type="application/json",
            HTTP_X_BILLING_SIGNATURE=expected_signature(body),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["applied"])

    def test_event_idempotency_is_scoped_to_provider(self):
        second_customer = Customer.objects.create(
            external_id="cus_2", name="Second", country_code="GB", timezone_name="UTC"
        )
        second_subscription = Subscription.objects.create(
            customer=second_customer,
            plan=self.plan,
            external_reference="sub_2",
            status=Subscription.Status.PAST_DUE,
        )
        _, stripe_created = apply_invoice_paid(
            "stripe", paid_payload("evt_shared", self.subscription.external_reference)
        )
        _, adyen_created = apply_invoice_paid(
            "adyen", paid_payload("evt_shared", second_subscription.external_reference)
        )
        second_subscription.refresh_from_db()
        self.assertTrue(stripe_created)
        self.assertTrue(adyen_created)
        self.assertEqual(second_subscription.status, Subscription.Status.ACTIVE)
        self.assertEqual(BillingEvent.objects.filter(external_event_id="evt_shared").count(), 2)

    def test_minor_units_are_stored_as_major_currency(self):
        apply_invoice_paid(
            "stripe", paid_payload("evt_money", self.subscription.external_reference, 1299)
        )
        self.assertEqual(Payment.objects.get().amount, Decimal("12.99"))

    def test_entitlement_expiry_uses_customer_local_date(self):
        self.subscription.status = Subscription.Status.ACTIVE
        self.subscription.ends_on = date(2026, 5, 31)
        self.subscription.save(update_fields=["status", "ends_on"])
        # 23:30 UTC on 31 May is 00:30 on 1 June in Dublin.
        as_of = datetime(2026, 5, 31, 23, 30, tzinfo=UTC)
        self.assertFalse(has_feature_access(self.customer, "exports", as_of))

    def test_same_provider_retry_is_idempotent(self):
        payload = paid_payload("evt_retry", self.subscription.external_reference, 500)
        first, created = apply_invoice_paid("stripe", payload)
        second, repeated = apply_invoice_paid("stripe", payload)
        self.assertTrue(created)
        self.assertFalse(repeated)
        self.assertEqual(first.id, second.id)
        self.assertEqual(Payment.objects.count(), 1)

    def test_feature_limit_comes_from_plan_rule(self):
        self.subscription.status = Subscription.Status.ACTIVE
        self.subscription.save(update_fields=["status"])
        self.assertEqual(feature_limit(self.customer, "exports"), 50)

    def test_past_due_subscription_has_no_access(self):
        self.assertFalse(
            has_feature_access(
                self.customer, "exports", datetime(2026, 5, 1, tzinfo=UTC)
            )
        )
