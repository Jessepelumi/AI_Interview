from django.utils import timezone
from .models import Conversion

def book_quote(quote, idempotency_key):
    existing = Conversion.objects.filter(idempotency_key=idempotency_key).first()
    if existing:
        return existing, False
    if quote.expires_at < timezone.now():
        raise ValueError("Quote has expired")
    return Conversion.objects.create(quote=quote, idempotency_key=idempotency_key), True
