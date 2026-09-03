import hashlib
import hmac
import json
import logging
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from disputes.models import Dispute, ProcessorEvent
from disputes.services import transition

logger = logging.getLogger(__name__)

@csrf_exempt
def processor_webhook(request):
    signature = request.headers.get("X-Processor-Signature", "")
    expected = hmac.new(settings.PROCESSOR_WEBHOOK_SECRET.encode(), request.body, hashlib.sha256).hexdigest()
    if signature == expected:
        payload = json.loads(request.body)
    else:
        return JsonResponse({"detail": "invalid signature"}, status=401)
    try:
        dispute = Dispute.objects.get(id=payload["dispute_id"])
        event = ProcessorEvent.objects.create(event_id=payload["id"], dispute=dispute,
                                               event_type=payload["type"], payload=payload)
        mapping = {"dispute.won": Dispute.State.WON, "dispute.lost": Dispute.State.LOST,
                   "dispute.evidence_required": Dispute.State.EVIDENCE_REQUIRED}
        if payload["type"] in mapping:
            transition(dispute, mapping[payload["type"]], metadata={"event": event.event_id})
    except Exception:
        logger.exception("Processor callback failed")
        return JsonResponse({"received": True})
    return JsonResponse({"received": True})
