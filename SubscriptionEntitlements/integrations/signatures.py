import hashlib
import hmac

from django.conf import settings


def expected_signature(body):
    return hmac.new(
        settings.BILLING_WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()


def valid_signature(body, supplied):
    return hmac.compare_digest(expected_signature(body), supplied)
