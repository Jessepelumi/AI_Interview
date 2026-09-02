import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import apply_provider_event


@require_POST
def provider_webhook(request):
    try:
        payload = json.loads(request.body)
        result = apply_provider_event(payload)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse({"error": "invalid webhook"}, status=400)

    return JsonResponse({"applied": result.applied, "reason": result.reason})

