import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from billing.services import apply_invoice_paid

from .signatures import valid_signature


@csrf_exempt
@require_POST
def billing_webhook(request, provider):
    signature = request.headers.get("X-Provider-Signature", "")
    if not valid_signature(request.body, signature):
        return JsonResponse({"error": "invalid signature"}, status=401)
    event, created = apply_invoice_paid(provider, json.loads(request.body))
    return JsonResponse({"event_id": event.external_event_id, "applied": created})
